#ToDo List
import os


class Person:
    def __init__(self, username, password):
        self.username = username
        self._password = password

    def check_password(self, password):
        return self._password == password


class User(Person):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def list_notes(self):
        if len(self.notes) == 0:
            print("Henüz not eklenmedi.")
        else:
            print("\nNotlarınız:")
            for i, note in enumerate(self.notes, start=1):
                print(str(i) + "-", note)

    def delete_note(self, note_number):
        if note_number >= 1 and note_number <= len(self.notes):
            removed_note = self.notes.pop(note_number - 1)
            print("Silinen not:", removed_note)
        else:
            print("Geçersiz not numarası.")


class FileManager:
    def __init__(self, users_file, notes_file):
        self.users_file = users_file
        self.notes_file = notes_file

    def create_files(self):
        if not os.path.exists(self.users_file):
            file = open(self.users_file, "w", encoding="utf-8")
            file.close()

        if not os.path.exists(self.notes_file):
            file = open(self.notes_file, "w", encoding="utf-8")
            file.close()

    def save_user(self, user):
        file = open(self.users_file, "a", encoding="utf-8")
        file.write(user.username + "," + user._password + "\n")
        file.close()

    def load_users(self):
        users = []

        file = open(self.users_file, "r", encoding="utf-8")
        lines = file.readlines()
        file.close()

        for line in lines:
            data = line.strip().split(",")

            if len(data) == 2:
                username = data[0]
                password = data[1]
                user = User(username, password)
                users.append(user)

        return users

    def save_note(self, username, note):
        file = open(self.notes_file, "a", encoding="utf-8")
        file.write(username + "," + note + "\n")
        file.close()

    def load_notes_for_user(self, user):
        file = open(self.notes_file, "r", encoding="utf-8")
        lines = file.readlines()
        file.close()

        for line in lines:
            data = line.strip().split(",", 1)

            if len(data) == 2:
                username = data[0]
                note = data[1]

                if username == user.username:
                    user.add_note(note)

    def rewrite_notes(self, user):
        all_lines = []

        file = open(self.notes_file, "r", encoding="utf-8")
        lines = file.readlines()
        file.close()

        for line in lines:
            data = line.strip().split(",", 1)

            if len(data) == 2:
                username = data[0]
                note = data[1]

                if username != user.username:
                    all_lines.append(line)

        for note in user.notes:
            all_lines.append(user.username + "," + note + "\n")

        file = open(self.notes_file, "w", encoding="utf-8")
        file.writelines(all_lines)
        file.close()


class App:
    def __init__(self):
        self.file_manager = FileManager("users.txt", "notes.txt")
        self.file_manager.create_files()
        self.users = self.file_manager.load_users()
        self.current_user = None

    def find_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None

    def register(self):
        print("\n--- KAYIT OL ---")
        username = input("Kullanıcı adı: ").strip()
        password = input("Şifre: ").strip()

        if username == "" or password == "":
            print("Alanlar boş olamaz.")
            return

        if self.find_user(username) is not None:
            print("Bu kullanıcı zaten kayıtlı.")
            return

        user = User(username, password)
        self.users.append(user)
        self.file_manager.save_user(user)

        print("Kayıt başarılı.")

    def login(self):
        print("\n--- GİRİŞ YAP ---")
        username = input("Kullanıcı adı: ").strip()
        password = input("Şifre: ").strip()

        user = self.find_user(username)

        if user is None:
            print("Kullanıcı bulunamadı.")
            return

        if user.check_password(password):
            self.current_user = user
            self.current_user.notes = []
            self.file_manager.load_notes_for_user(self.current_user)
            print("Giriş başarılı. Hoş geldin", self.current_user.username)
            self.user_menu()
        else:
            print("Şifre yanlış.")

    def user_menu(self):
        while True:
            print("\n--- KULLANICI MENÜSÜ ---")
            print("1 - Not ekle")
            print("2 - Notları listele")
            print("3 - Not sil")
            print("4 - Çıkış yap")

            choice = input("Seçiminiz: ").strip()

            if choice == "1":
                note = input("Notunuzu yazın: ").strip()

                if note == "":
                    print("Boş not eklenemez.")
                else:
                    self.current_user.add_note(note)
                    self.file_manager.save_note(self.current_user.username, note)
                    print("Not eklendi.")

            elif choice == "2":
                self.current_user.list_notes()

            elif choice == "3":
                self.current_user.list_notes()

                if len(self.current_user.notes) > 0:
                    try:
                        number = int(input("Silmek istediğiniz not numarası: "))
                        self.current_user.delete_note(number)
                        self.file_manager.rewrite_notes(self.current_user)
                    except ValueError:
                        print("Lütfen sayı girin.")

            elif choice == "4":
                print("Çıkış yapıldı.")
                self.current_user = None
                break

            else:
                print("Geçersiz seçim.")

    def main_menu(self):
        while True:
            print("\n===== ANA MENÜ =====")
            print("1 - Kayıt ol")
            print("2 - Giriş yap")
            print("3 - Programdan çık")

            choice = input("Seçiminiz: ").strip()

            if choice == "1":
                self.register()
            elif choice == "2":
                self.login()
            elif choice == "3":
                print("Program kapatılıyor...")
                break
            else:
                print("Geçersiz seçim.")


app = App()
app.main_menu()
