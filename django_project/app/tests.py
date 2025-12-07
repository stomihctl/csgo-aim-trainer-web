from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common import NoAlertPresentException
from selenium.webdriver import Keys

from app.models import *
from app.views import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.by import By
import time

# Create your tests here.

# class TestUrls(TestCase):
#     def test_home_is_resolved(self):
#         url = reversed('home')
#         self.assertEquals(resolve(url).func, home)

class TestViews(TestCase):
    def setUp(self):
        # Create users
        self.player_user = CustomUser.objects.create_user(username="player1", password="testpass", role="player")
        self.trainer_user = CustomUser.objects.create_user(username="trainer1", password="testpass", role="coach")
        self.admin_user = CustomUser.objects.create_user(username="admin1", password="testpass", role="admin")

        # Create related player/trainer
        self.player = Player.objects.create(playerid=self.player_user, nickname="P1", age=20, level="beginner")
        self.trainer = Trainer.objects.create(trainerid=self.trainer_user, expertise="aim", availability="weekdays")

        # Create base data
        self.exercise = Exercise.objects.create(name="Aiming Drill", description="Aim training", type="aim", difficulty="easy")

        self.plan = WeeklyPlan.objects.create(
            trainerid=self.trainer,
            playerid=self.player,
            creationdate=timezone.now(),
            status="active",
        )

        self.client = Client()

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_home_requires_login(self):
        response = self.client.get(reverse("home"))
        self.assertNotEqual(response.status_code, 404)
        #self.assertEqual(response.status_code, 200)

    def test_entry_test_page_loads(self):
        self.client.login(username="player1", password="testpass")
        response = self.client.get(reverse("entry_test"))
        self.assertEqual(response.status_code, 200)


    def test_account_remove_page_loads(self):
        self.client.login(username="admin1", password="testpass")
        response = self.client.get(reverse("account_remove"))
        self.assertEqual(response.status_code, 200)

    def test_attributes_input_page_loads(self):
        self.client.login(username="trainer1", password="testpass")
        response = self.client.get(reverse("attributes_input"))
        self.assertEqual(response.status_code, 200)

    # treba dodati da proverava da li ima trenera
    # def test_request_training_plan_page_loads(self):
    #     self.client.login(username="player1", password="testpass")
    #     response = self.client.get(reverse("request_training_plan"))
    #     self.assertEqual(response.status_code, 200)

    def test_request_training_plan_for_player(self):
        self.client.login(username="trainer1", password="testpass")
        response = self.client.get(reverse("request_training_plan_for_player", args=[self.player.pk]))
        self.assertEqual(response.status_code, 200)

    def test_trainer_selection_page_loads(self):
        self.client.login(username="player1", password="testpass")
        response = self.client.get(reverse("trainer_selection"))
        self.assertEqual(response.status_code, 200)

    def test_choose_trainer(self):
        self.client.login(username="player1", password="testpass")
        response = self.client.get(reverse("choose_trainer", args=[self.trainer.pk]))
        self.assertIn(response.status_code, [200, 302])

    def test_remove_chosen_trainer(self):
        self.client.login(username="player1", password="testpass")
        response = self.client.get(reverse("remove_chosen_trainer"))
        self.assertIn(response.status_code, [200, 302])

    def test_training_plan_generation_page_loads(self):
        self.client.login(username="trainer1", password="testpass")
        response = self.client.get(reverse("training_plan_generation"))
        self.assertEqual(response.status_code, 200)

    def test_training_statistics_page_loads(self):
        self.client.login(username="player1", password="testpass")
        response = self.client.get(reverse("training_statistics"))
        self.assertEqual(response.status_code, 200)

    #ako se ostave pocetna polja javlja gresku(value polje)
    def test_update_trainer_profile_page_loads(self):
        self.client.login(username="trainer1", password="testpass")
        response = self.client.get(reverse("update_trainer_profile"))
        self.assertEqual(response.status_code, 302)

    #promeniti
    def test_account_removal_request_page_loads(self):
        self.client.login(username="player1", password="testpass")
        response = self.client.get(reverse("account_removal_request"))
        self.assertEqual(response.status_code, 302)

    def test_single_training_request_page_loads(self):
        self.client.login(username="player1", password="testpass")
        response = self.client.get(reverse("single_training_request"))
        self.assertEqual(response.status_code, 200)

    def test_logoff_redirects(self):
        self.client.login(username="player1", password="testpass")
        response = self.client.get(reverse("logoff"))
        self.assertIn(response.status_code, [200, 302])




class ModelTests(TestCase):
    def setUp(self):
        # Kreiramo testne korisnike
        self.player_user = CustomUser.objects.create_user(
            username="player1", password="test12345", role="player"
        )
        self.trainer_user = CustomUser.objects.create_user(
            username="trainer1", password="test12345", role="coach"
        )

        # Kreiramo Player i Trainer instance
        self.player = Player.objects.create(
            playerid=self.player_user, nickname="P1", age=21, level="beginner"
        )
        self.trainer = Trainer.objects.create(
            trainerid=self.trainer_user,
            expertise="Aiming",
            availability="weekdays",
            priceperhour=10,
        )

    def test_player_creation(self):
        self.assertEqual(self.player.nickname, "P1")
        self.assertEqual(self.player.level, "beginner")
        self.assertEqual(self.player.playerid.username, "player1")

    def test_trainer_creation(self):
        self.assertEqual(self.trainer.trainerid.username, "trainer1")
        self.assertEqual(self.trainer.expertise, "Aiming")
        self.assertAlmostEqual(float(self.trainer.priceperhour), 10)

    def test_entry_test_model(self):
        entry = EntryTest.objects.create(
            playerid=self.player, datetaken=timezone.now().date(), score=15
        )
        self.assertEqual(entry.score, 15)
        self.assertEqual(entry.playerid, self.player)

    def test_account_deletion_request_model(self):
        req = AccountDeletionRequest.objects.create(
            userid=self.player_user,
            daterequested=timezone.now().date(),
            status="pending",
        )
        self.assertEqual(req.status, "pending")
        self.assertEqual(req.userid.username, "player1")

    def test_create_training_request(self):
        req = TrainingRequest.objects.create(
            playerid=self.player,
            trainerid=self.trainer,
            comment="I want to improve my reaction time",
            date=timezone.now().date(),
            status="pending",
        )
        self.assertEqual(req.comment, "I want to improve my reaction time")
        self.assertEqual(req.status, "pending")
        self.assertEqual(req.playerid.nickname, "P1")
        self.assertEqual(req.trainerid.trainerid.username, "trainer1")

    def test_training_request_default_status(self):
        req = TrainingRequest.objects.create(
            playerid=self.player, trainerid=self.trainer, comment=""
        )
        self.assertEqual(req.status, "pending")


# class FuntionalTestCase(StaticLiveServerTestCase):
#     def setUp(self):
#         self.browser = webdriver.Firefox()
#         self.appUrl = self.live_server_url + '/home'


class FunctionalTestCaseExerciseStat(StaticLiveServerTestCase):
    def setUp(self):
        chromedriver_autoinstaller.install()
        options = webdriver.ChromeOptions()
        # Uncomment da vidiš prozor
        # options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.browser = webdriver.Chrome(options=options)

        self.login_url = self.live_server_url + '/'
        self.home_url = self.live_server_url + '/home/'

        self.player_user = CustomUser.objects.create_user(username="player321", password="12345678", role="player")

        self.player = Player.objects.create(playerid=self.player_user, nickname="P1", age=20, level="beginner")

        self.exercise = Exercise.objects.create(
            exerciseid=2,  # opcionalno, Django će automatski dodeliti ID ako izostaviš
            name="DM HeadShot",
            description="Select in game gamemode deathmatch free for all and play it for 30 minuts. Focus on headshots.(number of hs is result for this exercise)",
            type="headshot",
            difficulty="hard"
        )

        Exercise.objects.create(name="Deathmatch", type="gamemode")

    def tearDown(self):
        # Zatvori browser nakon testa
        self.browser.quit()

    def test_login_and_open_home_page(self):
        """
        Test simulira:
        1. Otvori login stranicu
        2. Unese kredencijale
        3. Klikne Sign in
        4. Proveri da li je korisnik na /home
        """

        # Otvori login stranicu
        self.browser.get(self.login_url)
        time.sleep(1)  # da se stranica učita

        # Nađi inpute po id-jevima iz tvojeg HTML-a
        username_input = self.browser.find_element(By.XPATH, '//*[@id="login-identifier"]')
        password_input = self.browser.find_element(By.XPATH, '//*[@id="login-password"]')
        role_select = self.browser.find_element(By.XPATH, '//*[@id="login-role"]')

        # Unesi kredencijale (promeni ako treba da postojeći test korisnik)
        username_input.send_keys('player321')
        password_input.send_keys('12345678')
        role_select.send_keys('Player')

        time.sleep(2)

        # Klik na Sign in dugme
        login_button = self.browser.find_element(By.XPATH, '//*[@id="panel-login"]/div[5]/button[1]')
        login_button.click()

        # Sačekaj malo da se redirekcija izvrši
        time.sleep(2)

        # Ode direktno na home ako redirekcija nije automatska
        # self.browser.get(self.home_url)
        # time.sleep(1)

        next1 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next1.click()
        time.sleep(2)
        next2 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next2.click()
        time.sleep(2)
        next3 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next3.click()
        time.sleep(12)
        try:
            alert = self.browser.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            pass
        next5 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next5.click()
        time.sleep(2)

        time.sleep(2)

        trstat_req = self.browser.find_element(By.XPATH, '/html/body/nav/div[2]/a[2]')
        trstat_req.click()

        time.sleep(2)

        etype = self.browser.find_element(By.XPATH, '//*[@id="exercise"]')
        etype.send_keys('DM HeadShot')

        time.sleep(1)

        score = self.browser.find_element(By.XPATH, '//*[@id="score"]')
        score.send_keys('15')

        time.sleep(1)

        duration = self.browser.find_element(By.XPATH, '//*[@id="time"]')
        duration.send_keys('15')
        time.sleep(1)

        notes = self.browser.find_element(By.XPATH, '//*[@id="notes"]')
        notes.send_keys('great!')

        time.sleep(5)

        gen_btn = self.browser.find_element(By.XPATH, '//*[@id="statsForm"]/button')
        gen_btn.click()

        time.sleep(2)

        # Provera URL-a i sadržaja stranice
        # current_url = self.browser.current_url
        page_source = self.browser.page_source

        # self.assertIn('/single_training_request', current_url)
        self.assertTrue('Exercise statistics successfully saved!' in page_source)




class FunctionalTestCaseRequestAccRemoval(StaticLiveServerTestCase):
    def setUp(self):
        chromedriver_autoinstaller.install()
        options = webdriver.ChromeOptions()
        # Uncomment da vidiš prozor
        # options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.browser = webdriver.Chrome(options=options)

        self.login_url = self.live_server_url + '/'
        self.home_url = self.live_server_url + '/home/'

        self.player_user = CustomUser.objects.create_user(username="player321", password="12345678", role="player")

        self.player = Player.objects.create(playerid=self.player_user, nickname="P1", age=20, level="beginner")


        Exercise.objects.create(name="Deathmatch", type="gamemode")
    def tearDown(self):
        # Zatvori browser nakon testa
        self.browser.quit()

    def test_login_and_open_home_page(self):
        """
        Test simulira:
        1. Otvori login stranicu
        2. Unese kredencijale
        3. Klikne Sign in
        4. Proveri da li je korisnik na /home
        """

        # Otvori login stranicu
        self.browser.get(self.login_url)
        time.sleep(1)  # da se stranica učita

        # Nađi inpute po id-jevima iz tvojeg HTML-a
        username_input = self.browser.find_element(By.XPATH, '//*[@id="login-identifier"]')
        password_input = self.browser.find_element(By.XPATH, '//*[@id="login-password"]')
        role_select = self.browser.find_element(By.XPATH, '//*[@id="login-role"]')

        # Unesi kredencijale (promeni ako treba da postojeći test korisnik)
        username_input.send_keys('player321')
        password_input.send_keys('12345678')
        role_select.send_keys('Player')

        time.sleep(2)


        # Klik na Sign in dugme
        login_button = self.browser.find_element(By.XPATH, '//*[@id="panel-login"]/div[5]/button[1]')
        login_button.click()

        # Sačekaj malo da se redirekcija izvrši
        time.sleep(2)

        # Ode direktno na home ako redirekcija nije automatska
        # self.browser.get(self.home_url)
        # time.sleep(1)

        next1 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next1.click()
        time.sleep(2)
        next2 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next2.click()
        time.sleep(2)
        next3 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next3.click()
        time.sleep(12)
        try:
            alert = self.browser.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            pass
        next5 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next5.click()
        time.sleep(2)


        time.sleep(2)

        rem_req = self.browser.find_element(By.XPATH, '/html/body/nav/div[2]/form/button')
        rem_req.click()

        time.sleep(2)



        # Provera URL-a i sadržaja stranice
        #current_url = self.browser.current_url
        page_source = self.browser.page_source

        #self.assertIn('/single_training_request', current_url)
        self.assertTrue('Your account removal request has been submitted.' in page_source)

class FunctionalTestCaseRequestLogoff(StaticLiveServerTestCase):
    def setUp(self):
        chromedriver_autoinstaller.install()
        options = webdriver.ChromeOptions()
        # Uncomment da vidiš prozor
        # options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.browser = webdriver.Chrome(options=options)

        self.login_url = self.live_server_url + '/'
        self.home_url = self.live_server_url + '/home/'

        self.player_user = CustomUser.objects.create_user(username="player321", password="12345678", role="player")

        self.player = Player.objects.create(playerid=self.player_user, nickname="P1", age=20, level="beginner")


        Exercise.objects.create(name="Deathmatch", type="gamemode")
    def tearDown(self):
        # Zatvori browser nakon testa
        self.browser.quit()

    def test_login_and_open_home_page(self):
        """
        Test simulira:
        1. Otvori login stranicu
        2. Unese kredencijale
        3. Klikne Sign in
        4. Proveri da li je korisnik na /home
        """

        # Otvori login stranicu
        self.browser.get(self.login_url)
        time.sleep(1)  # da se stranica učita

        # Nađi inpute po id-jevima iz tvojeg HTML-a
        username_input = self.browser.find_element(By.XPATH, '//*[@id="login-identifier"]')
        password_input = self.browser.find_element(By.XPATH, '//*[@id="login-password"]')
        role_select = self.browser.find_element(By.XPATH, '//*[@id="login-role"]')

        # Unesi kredencijale (promeni ako treba da postojeći test korisnik)
        username_input.send_keys('player321')
        password_input.send_keys('12345678')
        role_select.send_keys('Player')

        time.sleep(2)


        # Klik na Sign in dugme
        login_button = self.browser.find_element(By.XPATH, '//*[@id="panel-login"]/div[5]/button[1]')
        login_button.click()

        # Sačekaj malo da se redirekcija izvrši
        time.sleep(2)

        # Ode direktno na home ako redirekcija nije automatska
        # self.browser.get(self.home_url)
        # time.sleep(1)

        next1 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next1.click()
        time.sleep(2)
        next2 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next2.click()
        time.sleep(2)
        next3 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next3.click()
        time.sleep(12)
        try:
            alert = self.browser.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            pass
        next5 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next5.click()
        time.sleep(2)


        time.sleep(2)

        logoff_req = self.browser.find_element(By.XPATH, '/html/body/nav/div[2]/a[6]')
        logoff_req.click()

        time.sleep(2)



        # Provera URL-a i sadržaja stranice
        current_url = self.browser.current_url
        page_source = self.browser.page_source

        self.assertIn('/', current_url)
        self.assertTrue('CS2 Trainer — Auth' in page_source)

class FunctionalTestCaseRequestSelectTrainer(StaticLiveServerTestCase):
    def setUp(self):
        chromedriver_autoinstaller.install()
        options = webdriver.ChromeOptions()
        # Uncomment da vidiš prozor
        # options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.browser = webdriver.Chrome(options=options)

        self.login_url = self.live_server_url + '/'
        self.home_url = self.live_server_url + '/home/'

        self.player_user = CustomUser.objects.create_user(username="player321", password="12345678", role="player")

        self.player = Player.objects.create(playerid=self.player_user, nickname="P1", age=20, level="beginner")

        self.trainer_user = CustomUser.objects.create_user(
            username="trainer123",
            password="87654321",
            role="coach"
        )

        self.trainer = Trainer.objects.create(
            trainerid=self.trainer_user,
            expertise="Aim improvement",
            availability="Weekdays",
            priceperhour=15.0
        )

        # Opcionalno dodati jezik i level trenera
        self.trainer_language = TrainerLanguage.objects.create(
            trainerid=self.trainer,
            language="English"
        )

        self.trainer_attribute = TrainerAttribute.objects.create(
            trainerid=self.trainer,
            level="Intermediate"
        )


        Exercise.objects.create(name="Deathmatch", type="gamemode")
    def tearDown(self):
        # Zatvori browser nakon testa
        self.browser.quit()

    def test_login_and_open_home_page(self):
        """
        Test simulira:
        1. Otvori login stranicu
        2. Unese kredencijale
        3. Klikne Sign in
        4. Proveri da li je korisnik na /home
        """

        # Otvori login stranicu
        self.browser.get(self.login_url)
        time.sleep(1)  # da se stranica učita

        # Nađi inpute po id-jevima iz tvojeg HTML-a
        username_input = self.browser.find_element(By.XPATH, '//*[@id="login-identifier"]')
        password_input = self.browser.find_element(By.XPATH, '//*[@id="login-password"]')
        role_select = self.browser.find_element(By.XPATH, '//*[@id="login-role"]')

        # Unesi kredencijale (promeni ako treba da postojeći test korisnik)
        username_input.send_keys('player321')
        password_input.send_keys('12345678')
        role_select.send_keys('Player')

        time.sleep(2)


        # Klik na Sign in dugme
        login_button = self.browser.find_element(By.XPATH, '//*[@id="panel-login"]/div[5]/button[1]')
        login_button.click()

        # Sačekaj malo da se redirekcija izvrši
        time.sleep(2)

        # Ode direktno na home ako redirekcija nije automatska
        # self.browser.get(self.home_url)
        # time.sleep(1)

        next1 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next1.click()
        time.sleep(2)
        next2 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next2.click()
        time.sleep(2)
        next3 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next3.click()
        time.sleep(12)
        try:
            alert = self.browser.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            pass
        next5 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next5.click()
        time.sleep(2)


        time.sleep(2)

        findt = self.browser.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/a')
        findt.click()

        time.sleep(2)

        findt = self.browser.find_element(By.XPATH, '/html/body/div/div/div[1]/div/form/button')
        findt.click()

        time.sleep(2)

        # Provera URL-a i sadržaja stranice
        current_url = self.browser.current_url
        page_source = self.browser.page_source

        self.assertIn('/home', current_url)
        self.assertTrue('You have successfully chosen' in page_source)

class FunctionalTestCaseARegistration(StaticLiveServerTestCase):
    def setUp(self):
        chromedriver_autoinstaller.install()
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # može da se vidi Chrome
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.browser = webdriver.Chrome(options=options)
        self.register_url = self.live_server_url + '/'
        self.home_url = self.live_server_url + '/home/'

    def tearDown(self):
        self.browser.quit()

    def test_registration_creates_user(self):
        # Otvori stranicu
        self.browser.get(self.register_url)
        time.sleep(1)
        create_acc_btn = self.browser.find_element(By.XPATH, '//*[@id="tab-register"]')
        create_acc_btn.click()

        # Nađi inpute po ID-jevima
        username_input = self.browser.find_element(By.ID, 'reg-username')
        email_input = self.browser.find_element(By.ID, 'reg-email')
        password_input = self.browser.find_element(By.ID, 'reg-password')
        password_confirm_input = self.browser.find_element(By.ID, 'reg-password2')
        role_select = self.browser.find_element(By.ID, 'reg-role')

        # Popuni formu
        username_input.send_keys('player321')
        email_input.send_keys('player321@example.com')
        password_input.send_keys('12345678')
        password_confirm_input.send_keys('12345678')
        role_select.send_keys('Player')

        terms_btn = self.browser.find_element(By.XPATH, '//*[@id="reg-consent"]')
        terms_btn.click()

        # Klik na Create account dugme
        register_button = self.browser.find_element(By.XPATH, '//*[@id="panel-register"]/div[5]/button[1]')
        register_button.click()

        # Sačekaj da server obradi
        time.sleep(5)

        # Provera da li je korisnik kreiran u bazi
        from app.models import CustomUser, Player
        user_exists = CustomUser.objects.filter(username='player321').exists()
        player_exists = Player.objects.filter(playerid__username='player321').exists()

        self.assertTrue(user_exists)
        self.assertTrue(player_exists)


class FunctionalTestCaseBLogin(StaticLiveServerTestCase):
    def setUp(self):
        chromedriver_autoinstaller.install()
        options = webdriver.ChromeOptions()
        # Uncomment da vidiš prozor
        # options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.browser = webdriver.Chrome(options=options)

        self.login_url = self.live_server_url + '/'
        self.home_url = self.live_server_url + '/home/'

        self.player_user = CustomUser.objects.create_user(username="player321", password="12345678", role="player")

        self.player = Player.objects.create(playerid=self.player_user, nickname="P1", age=20, level="beginner")

    def tearDown(self):
        # Zatvori browser nakon testa
        self.browser.quit()

    def test_login_and_open_home_page(self):
        """
        Test simulira:
        1. Otvori login stranicu
        2. Unese kredencijale
        3. Klikne Sign in
        4. Proveri da li je korisnik na /home
        """

        # Otvori login stranicu
        self.browser.get(self.login_url)
        time.sleep(1)  # da se stranica učita

        # Nađi inpute po id-jevima iz tvojeg HTML-a
        username_input = self.browser.find_element(By.XPATH, '//*[@id="login-identifier"]')
        password_input = self.browser.find_element(By.XPATH, '//*[@id="login-password"]')
        role_select = self.browser.find_element(By.XPATH, '//*[@id="login-role"]')

        # Unesi kredencijale (promeni ako treba da postojeći test korisnik)
        username_input.send_keys('player321')
        password_input.send_keys('12345678')
        role_select.send_keys('Player')

        time.sleep(2)


        # Klik na Sign in dugme
        login_button = self.browser.find_element(By.XPATH, '//*[@id="panel-login"]/div[5]/button[1]')
        login_button.click()

        # Sačekaj malo da se redirekcija izvrši
        time.sleep(2)

        # Ode direktno na home ako redirekcija nije automatska
        # self.browser.get(self.home_url)
        # time.sleep(1)

        # Provera URL-a i sadržaja stranice
        current_url = self.browser.current_url
        page_source = self.browser.page_source

        self.assertIn('/entry_test', current_url)
        self.assertTrue('Test' in page_source)

class FunctionalTestCaseExercise(StaticLiveServerTestCase):
    def setUp(self):
        chromedriver_autoinstaller.install()
        options = webdriver.ChromeOptions()
        # Uncomment da vidiš prozor
        # options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.browser = webdriver.Chrome(options=options)

        self.login_url = self.live_server_url + '/'
        self.home_url = self.live_server_url + '/home/'

        self.player_user = CustomUser.objects.create_user(username="player321", password="12345678", role="player")

        self.player = Player.objects.create(playerid=self.player_user, nickname="P1", age=20, level="beginner")

        self.exercise = Exercise.objects.create(
            exerciseid=2,  # opcionalno, Django će automatski dodeliti ID ako izostaviš
            name="DM HeadShot",
            description="Select in game gamemode deathmatch free for all and play it for 30 minuts. Focus on headshots.(number of hs is result for this exercise)",
            type="headshot",
            difficulty="hard"
        )

        Exercise.objects.create(name="Deathmatch", type="gamemode")
    def tearDown(self):
        # Zatvori browser nakon testa
        self.browser.quit()

    def test_login_and_open_home_page(self):
        """
        Test simulira:
        1. Otvori login stranicu
        2. Unese kredencijale
        3. Klikne Sign in
        4. Proveri da li je korisnik na /home
        """

        # Otvori login stranicu
        self.browser.get(self.login_url)
        time.sleep(1)  # da se stranica učita

        # Nađi inpute po id-jevima iz tvojeg HTML-a
        username_input = self.browser.find_element(By.XPATH, '//*[@id="login-identifier"]')
        password_input = self.browser.find_element(By.XPATH, '//*[@id="login-password"]')
        role_select = self.browser.find_element(By.XPATH, '//*[@id="login-role"]')

        # Unesi kredencijale (promeni ako treba da postojeći test korisnik)
        username_input.send_keys('player321')
        password_input.send_keys('12345678')
        role_select.send_keys('Player')

        time.sleep(2)


        # Klik na Sign in dugme
        login_button = self.browser.find_element(By.XPATH, '//*[@id="panel-login"]/div[5]/button[1]')
        login_button.click()

        # Sačekaj malo da se redirekcija izvrši
        time.sleep(2)

        # Ode direktno na home ako redirekcija nije automatska
        # self.browser.get(self.home_url)
        # time.sleep(1)

        next1 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next1.click()
        time.sleep(2)
        next2 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next2.click()
        time.sleep(2)
        next3 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next3.click()
        time.sleep(12)
        try:
            alert = self.browser.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            pass
        next5 = self.browser.find_element(By.XPATH, '//*[@id="next-btn"]')
        next5.click()
        time.sleep(2)


        time.sleep(2)

        ex_req = self.browser.find_element(By.XPATH, '/html/body/nav/div[2]/a[4]')
        ex_req.click()

        time.sleep(2)

        etype = self.browser.find_element(By.XPATH, '//*[@id="exerciseType"]')
        etype.send_keys('Shooting HS')

        time.sleep(5)

        gen_btn = self.browser.find_element(By.XPATH, '//*[@id="generateBtn"]')
        gen_btn.click()

        time.sleep(2)



        # Provera URL-a i sadržaja stranice
        #current_url = self.browser.current_url
        page_source = self.browser.page_source

        #self.assertIn('/single_training_request', current_url)
        self.assertTrue('Select in game gamemode deathmatch' in page_source)