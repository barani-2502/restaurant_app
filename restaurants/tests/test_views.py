from django.test import TestCase
from django.urls import reverse
from restaurants.models import Restaurant, Cuisine, MenuItem, Bookmark, Visit, Review
from django.core.paginator import Page
from django.contrib.auth import get_user_model
from django.core import mail


User = get_user_model()

class RestaurantListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass12345678')
        self.client.login(username='user', password='pass12345678')
        cuisine = Cuisine.objects.create(name="Indian")

        for i in range(12):
            restaurant = Restaurant.objects.create(
                name=f"Restaurant{i}",
                address = f'Address{i}',
                city="chennai",
                cost_for_two=500,
                food_type="veg",
                open_status=True,
                spotlight=False,
            )
            restaurant.cuisines.add(cuisine)

    def test_list_view_status_code(self):
        response = self.client.get(reverse('restaurant-list'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        response = self.client.get(reverse('restaurant-list'))

    def test_list_view_pagination_is_nine(self):
        response = self.client.get(reverse('restaurant-list'))
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['restaurants']), 9)

    def test_second_page_contains_remaining_restaurants(self):
        response = self.client.get(reverse('restaurant-list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['restaurants']), 3)

    def test_list_view_displays_restaurant_names(self):
        response = self.client.get(reverse('restaurant-list'))
        self.assertContains(response, "Restaurant0")
        self.assertContains(response, "Restaurant8")

class RestaurantDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass12345678')
        self.client.login(username='user', password='pass12345678')
        self.cuisine = Cuisine.objects.create(name="Indian")
        self.restaurant = Restaurant.objects.create(
            name= "ABC",
            address = "pallavaram",
            city="chennai",
            cost_for_two=500,
            food_type="veg",
            open_status=True,
            spotlight=False,
        )
        self.restaurant.cuisines.add(self.cuisine)

        self.menu_item1 = MenuItem.objects.create(
            restaurant=self.restaurant,
            name='Idli',
            price=30.0,
        )

        self.menu_item2 = MenuItem.objects.create(
            restaurant=self.restaurant,
            name='Dosa',
            price=60.0,
        )

    def test_detail_view_status_code(self):
        url = reverse('restaurant-detail', args=[self.restaurant.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        url = reverse('restaurant-detail', args=[self.restaurant.id])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'restaurants/restaurant_detail.html')

    def test_detail_view_context_contains_restaurant(self):
        url = reverse('restaurant-detail', args=[self.restaurant.id])
        response = self.client.get(url)
        self.assertEqual(response.context['restaurant'], self.restaurant)
    
    def test_invalid_restaurant_returns_404_error(self):
        url = reverse('restaurant-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class RegisterViewTests(TestCase):
    def setUp(self):
        self.url = reverse("register")

    def test_register_page_loads_successfully(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertContains(response, "Register")

    def test_register_creates_user_with_valid_data(self):
        data = {
            'username': "user",
            'email': 'test@gamil.com', 
            'password1': 'pass12345678',
            'password2': 'pass12345678',
        }

        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(User.objects.filter(username='user').exists())

    def test_register_creates_user_with_invalid_data(self):
        data = {
            'username': "user",
            'password1': 'pass12345678',
            'password2': 'pass12341234',
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertFalse(User.objects.filter(username='user').exists())

class LoginViewTests(TestCase):
    def setUp(self):
        self.username = "user"
        self.password = "pass12345678"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_url = reverse('login')
    
    def test_login_page_renders(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_login_with_valid_credentials(self):
        data = {"username": self.username, "password": self.password}
        response = self.client.post(self.login_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_login_with_invalid_credentials(self):
        data = {"username": self.username, "password": 'wrongpass'}
        response = self.client.post(self.login_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)

class LogoutViewTests(TestCase):
    def setUp(self):
        self.username = "user"
        self.password = "pass12345678"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')

    def test_logout_page_redirects(self):
        response = self.client.get(self.logout_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Find My Bite")

    def test_logout_functionality(self):
        self.client.get(self.logout_url, follow=True)
        response = self.client.get(self.home_url)
        self.assertFalse(response.context["user"].is_authenticated)

class PasswordChangeViewTests(TestCase):
    def setUp(self):
        self.username = "user"
        self.password = "pass12345678"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.password_change_url = reverse('password_change')
        self.password_change_done_url = reverse('password_change_done')
    
    def test_password_change_form_view_status_code(self):
        response = self.client.get(self.password_change_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_change_form.html')

    def test_password_change_done_view_status_code(self):
        response = self.client.get(self.password_change_done_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_change_done.html')

    def test_valid_password_change_redirects(self):
        data = {'old_password': self.password, 'new_password1': 'newpass12345678', 'new_password2': 'newpass12345678'}
        response = self.client.post(self.password_change_url, data)
        self.assertRedirects(response, self.password_change_done_url)

    def test_invalid_password_change_shows_error(self):
        data = {'old_password': 'wrongpass', 'new_password1': 'pass', 'new_password2': 'pass'}
        response = self.client.post(self.password_change_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your old password was entered incorrectly')

class PasswordResetViewTests(TestCase):
    def setUp(self):
        self.username = "user"
        self.email = "user@gmail.com"
        self.password = "pass12345678"
        User.objects.create_user(username=self.username, email=self.email, password=self.password)
        self.password_reset_url = reverse('password_reset')
        self.password_reset_done_url = reverse('password_reset_done')
        self.password_reset_confirm_url = reverse('password_reset_confirm', args=['uidb64', 'token'])
        self.password_reset_complete_url = reverse('password_reset_complete')

    def test_password_reset_page_loads(self):
        response = self.client.get(self.password_reset_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_form.html')

    def test_password_reset_email_sent_to_valid_user(self):
        response = self.client.post(self.password_reset_url, {'email': self.email})
        self.assertRedirects(response, self.password_reset_done_url)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Password reset', mail.outbox[0].subject)
        self.assertIn(self.email, mail.outbox[0].to)

    def test_password_reset_email_not_sent_to_invalid_user(self):
        response = self.client.post(self.password_reset_url, {'email': 'fake@fake.com'})
        self.assertRedirects(response, self.password_reset_done_url)
        self.assertEqual(len(mail.outbox), 0)

    def test_password_reset_done_view_loads(self):
        response = self.client.get(self.password_reset_done_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_done.html')

    def test_password_reset_complete_view_loads(self):
        response = self.client.get(self.password_reset_complete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_complete.html')

class ProfileViewTests(TestCase):
    def setUp(self):
        self.username = "user"
        self.email = "user@gmail.com"
        self.password = "pass12345678"
        User.objects.create_user(username=self.username, email=self.email, password=self.password)
        self.profile_url = reverse('profile')

    def test_profile_view_redirects_for_not_logged_in_user(self):
        response = self.client.get(self.profile_url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.profile_url}")
    
    def test_profile_view_loads_for_logged_in_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, 'Profile')
        self.assertContains(response, 'user@gmail.com')

class ProfileEditViewTests(TestCase):
    def setUp(self):
        self.username = "user"
        self.email = "user@gmail.com"
        self.password = "pass12345678"
        self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        self.profile_edit_url = reverse('profile_edit')

    def test_profile_edit_page_loads_successfully_for_logged_in_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.profile_edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile_edit.html')
        self.assertContains(response, 'Save Changes')
        self.assertContains(response, 'user@gmail.com')

    def test_profile_edit_page_redirects_for_not_logged_in_user(self):
        self.client.logout()
        response = self.client.get(self.profile_edit_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_valid_profile_edit_updates_profile_data(self):
        self.client.login(username=self.username, password=self.password)
        valid_data = {
            'first_name': 'first',
            'last_name': 'last',
            'email': 'firstlast@findmybite.com',
        }

        response = self.client.post(self.profile_edit_url, valid_data, follow=True)
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'first')
        self.assertEqual(self.user.last_name, 'last')
        self.assertEqual(self.user.email, 'firstlast@findmybite.com')


    def test_invalid_profile_edit_shows_errors(self):
        self.client.login(username=self.username, password=self.password)
        invalid_data = {
            'first_name': '',
            'last_name': '',
            'email': 'fake%',
        }

        response = self.client.post(self.profile_edit_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile_edit.html')
        self.assertContains(response, 'Enter a valid email address')

class BookmarkViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            password='pass12345678',
        )
        self.restaurant = Restaurant.objects.create(
            name="ABC",
            address="pallavaram",
            city="chennai",
            cost_for_two=500,
            food_type="veg",
            open_status=True,
            spotlight=False,
        )
        self.bookmarks_list_url = reverse('bookmarks_list')

    def test_bookmark_list_view_requires_login(self):
        response = self.client.get(self.bookmarks_list_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_bookmark_list_view_displays_user_bookmarks(self):
        self.client.login(username='user', password='pass12345678')
        Bookmark.objects.create(user=self.user, restaurant=self.restaurant)
        response = self.client.get(self.bookmarks_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/bookmarks_list.html')
        self.assertContains(response, self.restaurant.name)
        self.assertEqual(len(response.context['bookmarked_restaurants']), 1)

    def test_bookmark_list_empty_state(self):
        self.client.login(username='user', password='pass12345678')
        response = self.client.get(self.bookmarks_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No restaurants found.")
        self.assertEqual(len(response.context['bookmarked_restaurants']), 0)

class BookmarkToggleViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass12345678')
        self.restaurant = Restaurant.objects.create(
            name="A2B",
            address = "Pallavaram",
            city="chennai",
            cost_for_two=500,
            food_type="veg",
            open_status=True,
            spotlight=False,
        )
        self.bookmarks_list_url = reverse('bookmarks_list')
        self.toggle_url = reverse('bookmark_toggle', args=[self.restaurant.id])

    def test_bookmark_toggle_creates_bookmark_if_not_present(self):
        self.client.login(username='user', password='pass12345678')
        self.assertFalse(Bookmark.objects.filter(user=self.user, restaurant=self.restaurant).exists())
        response = self.client.post(self.toggle_url)
        self.assertRedirects(response, self.bookmarks_list_url)
        self.assertTrue(Bookmark.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_bookmark_toggle_deletes_bookmark_if_already_present(self):
        self.client.login(username='user', password='pass12345678')
        Bookmark.objects.create(user=self.user, restaurant=self.restaurant)
        self.assertTrue(Bookmark.objects.filter(user=self.user, restaurant=self.restaurant).exists())
        response = self.client.post(self.toggle_url)
        self.assertRedirects(response, self.bookmarks_list_url)
        self.assertFalse(Bookmark.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_redirect_if_not_logged_in(self):
        response = self.client.post(self.toggle_url)
        login_url = reverse('login')
        self.assertRedirects(response, f'{login_url}?next={self.toggle_url}')

    def test_bookmark_toggle_redirects_to_next_url(self):
        self.client.login(username='user', password='pass12345678')
        home_url = reverse('home')
        response = self.client.post(self.toggle_url, {'next': home_url})
        self.assertRedirects(response, home_url)

class VisitViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass12345678')
        self.restaurant = Restaurant.objects.create(
            name="A2B",
            address = "Pallavaram",
            city="chennai",
            cost_for_two=500,
            food_type="veg",
            open_status=True,
            spotlight=False,
        )
        self.visited_restaurants_list_url = reverse('visited_restaurants_list')

    def test_visited_restaurants_view_requires_login(self):
        response = self.client.get(self.visited_restaurants_list_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_visited_restaurants_view_displays_user_visits(self):
        self.client.login(username='user', password='pass12345678')
        Visit.objects.create(user=self.user, restaurant=self.restaurant)
        response = self.client.get(self.visited_restaurants_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/visited_restaurants_list.html')
        self.assertContains(response, self.restaurant.name)

    def test_visited_restaurants_list_empty_state(self):
        self.client.login(username='user', password='pass12345678')
        response = self.client.get(self.visited_restaurants_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No restaurants found.")
        self.assertEqual(len(response.context['visited_restaurants']), 0)

class VisitToggleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass12345678')
        self.restaurant = Restaurant.objects.create(
            name="A2B",
            address = "Pallavaram",
            city="chennai",
            cost_for_two=500,
            food_type="veg",
            open_status=True,
            spotlight=False,
        )
        self.toggle_url = reverse('visited_toggle', args=[self.restaurant.id])

    def test_redirect_if_not_logged_in(self):
        response = self.client.post(self.toggle_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_visited_toggle_adds_visited_if_not_present(self):
        self.client.login(username="user", password="pass12345678")
        response = self.client.post(self.toggle_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Visit.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_visited_toggle_removes_visited_if_already_present(self):
        Visit.objects.create(user=self.user, restaurant=self.restaurant)
        self.client.login(username="user", password="pass12345678")
        response = self.client.post(self.toggle_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Visit.objects.filter(user=self.user, restaurant=self.restaurant).exists())

class ReviewCreateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass12345678')
        self.restaurant = Restaurant.objects.create(
            name="A2B",
            address = "Pallavaram",
            city="chennai",
            cost_for_two=500,
            food_type="veg",
            open_status=True,
            spotlight=False,
        )
    
    def test_create_review_requires_login(self):
        url = reverse('add_review', kwargs={'pk': self.restaurant.pk})
        data = {'title':'ok', 'rating':4, 'comment': 'nice food' }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_create_view_creates_review_successfully(self):
        data = {'title':'ok', 'rating':4, 'comment': 'nice food' }
        self.client.login(username='user', password='pass12345678')
        url = reverse('add_review', kwargs={'pk':self.restaurant.pk})
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Review.objects.filter(user=self.user, restaurant=self.restaurant).exists())
        review = Review.objects.get(user=self.user, restaurant=self.restaurant)
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, 'nice food')

class ReviewUpdateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass12345678')
        self.restaurant = Restaurant.objects.create(
            name="A2B",
            address = "Pallavaram",
            city="chennai",
            cost_for_two=500,
            food_type="veg",
            open_status=True,
            spotlight=False,
        )

    def test_update_view_requires_login(self):
        url = reverse('edit_review', kwargs={'pk': self.restaurant.pk})
        data = {'title':'ok', 'rating':4, 'comment': 'nice food' }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_update_view_updates_review_successfully(self):
        review = Review.objects.create(user=self.user, restaurant=self.restaurant, rating=3, comment='Okay food')
        self.client.login(username="user", password="pass12345678")
        url = reverse('edit_review', kwargs={'pk': review.pk})
        updated_data = {'rating': 5, 'title':'great' ,'comment': 'Amazing food!'}
        response = self.client.post(url, updated_data, follow=True)
        self.assertEqual(response.status_code, 200)
        review.refresh_from_db()
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Amazing food!')

class ReviewDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass12345678')
        self.restaurant = Restaurant.objects.create(
            name="A2B",
            address = "Pallavaram",
            city="chennai",
            cost_for_two=500,
            food_type="veg",
            open_status=True,
            spotlight=False,
        )

    def test_delete_view_requires_login(self):
        url = reverse('delete_review', kwargs={'pk': self.restaurant.pk})
        data = {'title':'ok', 'rating':4, 'comment': 'nice food' }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_delete_view_deletes_review_successfully(self):
        review = Review.objects.create(user=self.user, restaurant=self.restaurant, rating=4, comment='Good')
        self.client.login(username="user", password="pass12345678")
        url = reverse('delete_review', kwargs={'pk': review.pk})
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Review.objects.filter(pk=review.pk).exists())
