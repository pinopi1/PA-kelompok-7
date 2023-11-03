import csv
import datetime
import pwinput
from prettytable import PrettyTable

e_money_balance = 0  # Variabel saldo e-money global
current_time = datetime.datetime.now()

# Fungsi untuk mendaftarkan akun baru
def register_account():
    while True:
        username = input(" > Masukkan username baru: ").strip()
        if not username:
            print("Username tidak boleh kosong. Silakan coba lagi.")
            continue
        elif not username.isalnum():
            print("Username hanya boleh mengandung huruf dan angka. Silakan coba lagi.")
            continue

        password = pwinput.pwinput(" > Masukkan password baru: ", mask="*").strip()
        if not password:
            print("Password tidak boleh kosong. Silakan coba lagi.")
            continue
        elif not password.isalnum():
            print("Password hanya boleh mengandung huruf dan angka. Silakan coba lagi.")
            continue
        elif len(password) < 5:
            print("Password terlalu pendek. Password harus minimal 5 karakter.")
            continue
        elif len(password) > 15:
            print("Password terlalu panjang. Password harus maksimal 15 karakter.")
            continue

        while True:
            confirm_password = pwinput.pwinput(" > Konfirmasi password: ", mask="*")
            if password == confirm_password:
                break
            else:
                print("Password tidak cocok. Silakan coba lagi.")

        role = 'user'

        with open('datausers.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username:
                    print("Username sudah terdaftar. Silakan coba lagi.")
                    return

        # Meminta pengguna untuk mengisi saldo e-money saat mendaftar
        while True:
            try:
                e_money_balance = float(input(" > Masukkan saldo e-money: "))
                if e_money_balance < 0:
                    print("Saldo e-money tidak boleh negatif. Silakan coba lagi.")
                else:
                    break
            except ValueError:
                print("Saldo e-money harus berupa angka. Silakan coba lagi.")

        with open('datausers.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password, role, e_money_balance])
            print("Akun berhasil didaftarkan. Silakan Login!")
            break

# Fungsi untuk menambahkan akun admin baru
def add_admin_account():
    admin_password = pwinput.pwinput(" > Masukkan kata sandi admin: ", mask="*")
    with open('datausers.csv', mode='r') as file:
        reader = csv.reader(file)
        data = list(reader)

    admin_found = False
    for row in data:
        if row[1] == admin_password and row[2] == 'admin':
            admin_found = True
            break

    if admin_found:
        while True:
            admin_username = input(" > Masukkan username admin baru: ").strip()
            if not admin_username:
                print("Username tidak boleh kosong. Silakan coba lagi.")
                continue
            elif not admin_username.isalnum():
                print("Username hanya boleh mengandung huruf dan angka. Silakan coba lagi.")
                continue

            password = pwinput.pwinput(" > Masukkan password baru: ", mask="*").strip()
            if not password:
                print("Password tidak boleh kosong. Silakan coba lagi.")
                continue
            elif not password.isalnum():
                print("Password hanya boleh mengandung huruf dan angka. Silakan coba lagi.")
                continue
            elif len(password) < 5:
                print("Password terlalu pendek. Password harus minimal 5 karakter.")
                continue
            elif len(password) > 15:
                print("Password terlalu panjang. Password harus maksimal 15 karakter.")
                continue

            while True:
                confirm_password = pwinput.pwinput(" > Konfirmasi password: ", mask="*")
                if password == confirm_password:
                    break
                else:
                    print("Password tidak cocok. Silakan coba lagi.")                

            new_admin_data = [admin_username, admin_password, 'admin']

            with open('datausers.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(new_admin_data)
            print(f"Akun admin {admin_username} berhasil ditambahkan.")
            break
    else:
        print("Kata sandi admin salah atau tidak memiliki izin.")

# Fungsi untuk menampilkan daftar akun (hanya untuk admin)
def list_accounts():
    with open('datausers.csv', mode='r') as file:
        reader = csv.reader(file)
        table = PrettyTable()
        table.field_names = ["Username", "Role"]

        for row in reader:
            table.add_row([row[0], row[2]])

        print(table)

username = {}

# Fungsi untuk melakukan login
def login():
    global e_money_balance  # Tambahkan ini
    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        username = input(" > Masukkan username: ")
        password = pwinput.pwinput(" > Masukkan password: ", mask="*")

        with open('datausers.csv', mode='r') as file:
            reader = csv.reader(file)
            user_found = False
            for row in reader:
                if row[0] == username and row[1] == password:
                    if row[2] == 'admin':
                        admin_access_code = pwinput.pwinput(" > Masukkan kode akses admin: ", mask="*")
                        if admin_access_code == "admin1":
                            return username, row[2]
                        else:
                            print("Kode akses admin salah.")
                            user_found = True
                            break
                    else:
                        e_money_balance = float(row[3])  # Ambil saldo e-money
                        return username, row[2]
            if not user_found:
                print("Username atau password salah.")
                attempts += 1
                remaining_attempts = max_attempts - attempts
                if remaining_attempts > 0:
                    print(f"Anda memiliki {remaining_attempts} kesempatan lagi.")
                else:
                    print("Anda telah mencapai batas maksimum percobaan. Silahkan Login ulang!")
                    return None, None

    print("Anda telah mencapai batas maksimum percobaan. Silakan Login ulang!")
    return None, None

# Fungsi untuk menghapus akun
# Fungsi untuk menghapus akun (hanya untuk admin)
def delete_account():
    if role != 'admin':
        print("Anda tidak memiliki izin untuk menghapus akun.")
        return

    admin_password = pwinput.pwinput(" > Password Admin: ", mask="*")

    with open('datausers.csv', mode='r') as file:
        reader = csv.reader(file)
        data = list(reader)

    admin_found = False
    user_found = False

    for row in data:
        if row[1] == admin_password and row[2] == 'admin':
            admin_found = True

    if admin_found:
        table = PrettyTable()
        table.field_names = ["Username", "Password", "Role"]  # Add the appropriate field names

        for row in data:
            table.add_row(row[:3])  # Add only the first three values (Username, Password, Role)

        print("Data Seluruh Akun:")
        print(table)

        username_to_delete = input(" > Masukkan username yang akan dihapus: ")

        for row in data:
            if row[0] == username_to_delete:
                user_found = True

        if user_found:
            confirm_delete = input(f" >> Konfirmasi: Apakah Anda yakin ingin menghapus akun {username_to_delete}? (ya/tidak): ")
            if confirm_delete.lower() == 'ya' or confirm_delete.lower() == 'y':
                data = [row for row in data if row[0] != username_to_delete]

                with open('datausers.csv', mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(data)
                print(f"Akun {username_to_delete} telah dihapus.")
            elif confirm_delete.lower() == "tidak" or confirm_delete.lower() == "t":
                print("Penghapusan dibatalkan.")
            else:
                print("Masukan tidak valid. Penghapusan dibatalkan.")
        else:
            print("Akun yang akan dihapus tidak ditemukan.")
    else:
        print("Tidak ada izin atau data yang tidak sesuai.")

# Fungsi untuk mengelola akun (hanya untuk admin)
def manage_accounts():
    while True:
        print("\n")
        print(16*"_")
        print("-- Kelola Akun --")
        print(16*"-")
        print("1. Tampilkan Daftar Akun")
        print("2. Tambah Akun Admin")
        print("3. Hapus Akun")
        print("4. Kembali ke Menu Admin")
        choice = input("> Pilih opsi: ")

        if choice == '1':
            list_accounts()
        elif choice == '2':
            add_admin_account()
        elif choice == '3':
            delete_account()
        elif choice == '4':
            break
        else:
            print("Opsi tidak valid. Silakan pilih lagi.")

# Fungsi untuk mengelola lagu (hanya untuk admin)
# Fungsi untuk mengelola lagu (hanya untuk admin)
def manage_songs():
    while True:
        print("\n")
        print(16*"_")
        print("-- Kelola Lagu --")
        print(16*"-")
        # Menampilkan daftar lagu menggunakan PrettyTable
        with open('daftarmusik.csv', mode='r') as file:
            csv_reader = csv.reader(file)
            table = PrettyTable()
            table.field_names = ["Judul Lagu", "Artis", "Harga"]
            for row in csv_reader:
                table.add_row([row[0], row[1], row[2]])
            print(table,"\n")

        print("1. Tambah Lagu")
        print("2. Update Lagu")
        print("3. Hapus Lagu")
        print("4. Urutkan Lagu")
        print("5. Cari Lagu")
        print("6. Kembali ke Menu Admin")
        choice = input("> Pilih opsi: ")

        if choice == '1':
            add_song()
        elif choice == '2':
            update_song()
        elif choice == '3':
            delete_song()
        elif choice == '4':
            sort_songs()
        elif choice == '5':
            search_song()
        elif choice == '6':
            break
        else:
            print("Opsi tidak valid. Silakan pilih lagi.")

# Fungsi untuk menambahkan lagu baru
def add_song():
    while True:
        song_name = input(" > Masukkan nama lagu: ")

        # Memeriksa apakah nama lagu hanya berisi huruf dan angka
        if not song_name.replace(' ', '').isalnum():
            print("Nama lagu tidak valid. Nama lagu harus berisi huruf dan angka.")
            continue

        artist_name = input(" > Masukkan nama artis: ")
        price = float(input(" > Masukkan harga lagu: "))

        with open('daftarmusik.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([song_name, artist_name, price])
        print("Lagu berhasil ditambahkan.")
        break

# Fungsi untuk menampilkan semua lagu
def show_songs():
    table = PrettyTable()
    table.field_names = ["Judul Lagu", "Artis", "Harga"]

    with open('daftarmusik.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            table.add_row([row[0], row[1], row[2]])

    print(table)

def update_song():
    song_name = input("Masukkan nama lagu yang ingin diupdate: ")
    with open('daftarmusik.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        data = [row for row in csv_reader]

        for row in data:
            if row[0] == song_name:
                print(f"Update lagu: {row[0]} by {row[1]}, Price: {row[2]}")
                new_name = input("Masukkan nama lagu baru (kosongkan jika tidak ingin mengubah): ")
                new_artist = input("Masukkan nama artis baru (kosongkan jika tidak ingin mengubah): ")
                new_price = input("Masukkan harga lagu baru (kosongkan jika tidak ingin mengubah): ")

                if new_name:
                    row[0] = new_name
                if new_artist:
                    row[1] = new_artist
                if new_price:
                    row[2] = new_price

                with open('daftarmusik.csv', mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(header)
                    writer.writerows(data)
                print("Lagu berhasil diupdate.")
                return

        print(f"Lagu '{song_name}' tidak ditemukan.")

# Fungsi untuk menampilkan semua lagu
def show_songs():
    table = PrettyTable()
    table.field_names = ["Judul Lagu", "Artis", "Harga"]

    with open('daftarmusik.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            table.add_row([row[0], row[1], row[2]])

    print(table)

# Fungsi untuk menghapus lagu (hanya untuk admin)
def delete_song():
    song_name = input(" > Masukkan nama lagu yang ingin dihapus: ")
    with open('daftarmusik.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        data = [row for row in csv_reader]

        for row in data:
            if row[0] == song_name:
                data.remove(row)

                with open('daftarmusik.csv', mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(header)
                    writer.writerows(data)
                print(f"Lagu '{song_name}' berhasil dihapus.")
                return

        print(f"Lagu '{song_name}' tidak ditemukan.")

# Fungsi untuk mencari lagu berdasarkan judul atau nama artis
def search_song():
    search_term = input(" > Masukkan nama artis: ").lower()
    found_songs = []

    with open('daftarmusik.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Lewati baris header
        for row in csv_reader:
            artist_name = row[1].lower()

            if search_term in artist_name or search_term in artist_name:
                found_songs.append(row)

    if found_songs:
        table = PrettyTable()
        table.field_names = ["Judul Lagu", "Artis", "Harga"]

        for song in found_songs:
            table.add_row(song)

        print("Hasil Pencarian:")
        print(table)

        # Memproses pembelian jika lagu ditemukan
        while True:
            choice = input(" > Pilih opsi:\n1. Beli Lagu\n2. Kembali\n> ")

            if choice == '1':
                # Memproses pembelian lagu
                buy_song()
                break
            elif choice == '2':
                break
            else:
                print("Opsi tidak valid. Silakan pilih lagi.")
    else:
        print("Lagu tidak ditemukan.")

# Fungsi untuk mengurutkan lagu berdasarkan judul atau harga
def sort_songs():
    sort_option = input(" > Urutkan berdasarkan (song/price): ").lower()
    with open('daftarmusik.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        data = [row for row in csv_reader]
        # .sort()

        if sort_option == 'song':
            data.sort(key=lambda x: x[0])
        elif sort_option == 'price':
            data.sort(key=lambda x: float(x[2]))

    with open('daftarmusik.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)
    print("Daftar lagu berhasil diurutkan.")

def record_purchase(username, song_name, artist_name, price):
    # Open "purchased_songs.csv" in append mode and write the purchase record
    with open('purchased_songs.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, song_name, artist_name, price])

# Fungsi untuk melakukan transaksi pembelian lagu
def buy_song():
    global e_money_balance
    song_name = input(" > Masukkan nama lagu yang ingin dibeli: ")
    song_found = False  # Variabel untuk melacak apakah lagu ditemukan
    
    purchased_songs = []

    # Membaca file "purchased_songs.csv" untuk melihat playlist lagu yang telah dibeli oleh pengguna
    try:
        # Membaca file "purchased_songs.csv" untuk melihat playlist lagu yang telah dibeli oleh pengguna
        with open('purchased_songs.csv', mode='r') as file:
            csv_reader = csv.reader(file)
            try:
                header = next(csv_reader)

                # Populate the purchased_songs list
                for row in csv_reader:
                    if row[0] == username:
                        purchased_songs.append(row[1])
            except StopIteration:
                # Handle the case where the file is empty
                pass
    except FileNotFoundError:
        # Handle the case where the file doesn't exist
        pass

    if song_name in purchased_songs:
        print("Anda telah membeli lagu ini sebelumnya.")
        return  # Keluar dari fungsi jika lagu sudah ada dalam playlist

    # Lanjutkan proses pembelian jika lagu belum dibeli
    with open('daftarmusik.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        data = [row for row in csv_reader]

        for row in data:
            if row[0] == song_name:
                price = float(row[2])
                if e_money_balance >= price:
                    # Meminta konfirmasi pembelian
                    while True:
                        confirm_purchase = input(" >> Konfirmasi pembelian (y/n): ").lower()
                        if confirm_purchase == "y":
                            # Menyimpan data pembelian ke dalam file "purchased_songs.csv"
                            record_purchase(username, song_name, row[1], price)
                            current_time = datetime.datetime.now()
                            print(28*"-")
                            print("     Invoice Pembelian:")
                            print(28*"-")
                            print(f"{current_time}","\n")
                            print(f"Judul Lagu: {song_name}")
                            print(f"Artis: {row[1]}")
                            print(f"Harga: {price}")
                            print(f"Saldo E-money Terakhir: {e_money_balance}","\n")
                            e_money_balance -= price
                            # Perbarui saldo dalam file CSV
                            update_balance_in_csv(username, e_money_balance)
                            break
                        elif confirm_purchase == "n":
                            print("Pembelian dibatalkan.")
                            break
                        else:
                            print("Masukan tidak valid. Silakan ketik 'y' atau 'n'.")

                    song_found = True  # Menandai lagu ditemukan
                    break  # Keluar dari loop setelah menemukan lagu

    if not song_found:
        print(f"Lagu '{song_name}' tidak ditemukan.")  # Hanya tampilkan pesan jika lagu tidak ditemukan

# Fungsi untuk top-up e-money
def top_up_emoney(username, e_money_balance):
    while True:
        try:
            print(f"Saldo e-money Anda: {e_money_balance}")
            amount = float(input(" > Masukkan jumlah top-up: "))
            if amount > 0:
                print(f"Konfirmasi top-up sebesar {amount}.")
                confirm = input(f" >> Lanjutkan? (y/n): ").lower()
                if confirm == "y":
                    e_money_balance += amount
                    print(f"Saldo e-money Anda sekarang: {e_money_balance}")
                    # Perbarui saldo dalam file CSV
                    update_balance_in_csv(username, e_money_balance)
                    return e_money_balance  # Mengembalikan saldo yang baru diperbarui
                elif confirm == "n":
                    print("Top-up dibatalkan.")
                    return e_money_balance  # Mengembalikan saldo yang tidak berubah
                else:
                    print("Masukan tidak valid. Silakan ketik 'y' atau 'n'.")
            else:
                print("Jumlah top-up harus positif. Silakan coba lagi.")
        except ValueError:
            print("Masukkan harus berupa angka. Silakan coba lagi.")
        return e_money_balance  # Mengembalikan saldo yang tidak berubah jika top-up tidak berhasil

def update_balance_in_csv(username, new_balance):
    data = []

    with open('datausers.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username:
                row[3] = new_balance
            data.append(row)

    with open('datausers.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
        
def purchased_songs():
    # Membaca file CSV "purchased_songs.csv" dan menampilkan lagu-lagu yang telah dibeli oleh pengguna.
    with open('purchased_songs.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Lewati baris header
        purchased_songs = []
        for row in csv_reader:
            if row[0] == username:
                purchased_songs.append(row[1:4])  # Ambil judul lagu, artis, dan harga

    if purchased_songs:
        # Buat objek PrettyTable
        table = PrettyTable()
        table.field_names = ["Judul Lagu", "Artis", "Harga"]

        for song in purchased_songs:
            table.add_row([song[0], song[1], song[2]])

        print("Playlist Lagu yang Sudah Dibeli:")
        print(table)
    else:
        print("Anda belum membeli lagu apa pun.")



# Program utama
is_admin_logged_in = False

while True:
    
    try:
    # Menampilkan menu utama dan meminta pilihan pengguna.
        print(21*"=")
        print("-- Selamat datang! --")
        print(21*"=")
        print("1. Login")
        print("2. Sign Up")
        print("3. Keluar")
        choice = input("> Pilih opsi: ")

        # Melakukan tindakan yang sesuai berdasarkan pilihan pengguna.
        if choice == '1':
            username, role = login()
            if role is not None:
                print("\n")
                print(f"Selamat datang, {role.capitalize()} {username.capitalize()}!")

                # Tambahkan kondisi untuk hanya menampilkan saldo jika peran adalah "user"
                if role == 'user':
                    print(f"Saldo e-money Anda: {e_money_balance}")

                if role == 'admin':
                    is_admin_logged_in = True
                    # Menu Admin
                    while True:
                        
                        print(16*"_")
                        print("-- Menu Admin --")
                        print(16*"-")
                        print("1. Kelola Akun")
                        print("2. Kelola Lagu")
                        print("3. Logout")
                        choice = input("> Pilih opsi: ")

                        if choice == '1' and is_admin_logged_in:
                            manage_accounts()
                        elif choice == '2':
                            manage_songs()
                        elif choice == '3':
                            print("Anda telah Logout.")
                            print("\n")
                            break
                        else:
                            print("Opsi tidak valid. Silakan pilih lagi.")

                elif role == "user":
                    # Menu User
                    while True:
                        print("\n")
                        print(21*"=")
                        print("-- Menu User --")
                        print(21*"=")
                        print(current_time)
                        print(f"Username: {username.capitalize()}")
                        print(f"E-money: {e_money_balance}", "\n")
                        with open('daftarmusik.csv', mode='r') as file:
                            csv_reader = csv.reader(file)
                            table = PrettyTable()
                            table.field_names = ["Judul Lagu", "Artis", "Harga"]
                            for row in csv_reader:
                                table.add_row([row[0], row[1], row[2]])
                            print(table,"\n")

                        print("1. Cari Lagu")
                        print("2. Lihat playlist")
                        print("3. Beli Lagu")
                        print("4. Top-up e-money")
                        print("5. Logout")
                        choice = input("> Pilih opsi: ")

                        if choice == '1':
                            search_song()
                        elif choice == '2':
                            purchased_songs()
                        elif choice == '3':
                            buy_song()
                        elif choice == '4':
                            e_money_balance = top_up_emoney(username, e_money_balance)  # Menambahkan parameter username dan e_money_balance
                        elif choice == '5':
                            print("Anda telah Logout.")
                            print("\n")
                            break
                        else:
                            print("Opsi tidak valid. Silakan pilih lagi.")
                            
        elif choice == '2':
            register_account()

        elif choice == '3':
            print(31*"=")
            print("-- Makasih! Selamat tinggal. --")
            print(31*"=")
            break

        else:
            print("Opsi tidak valid. Silakan pilih lagi.")
            
    except KeyboardInterrupt:
            print("Program dihentikan oleh pengguna.")
            is_admin_logged_in = True
