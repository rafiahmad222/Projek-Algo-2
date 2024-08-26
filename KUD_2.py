import psycopg2 
import os 
import tabulate
from rich import print 
import datetime
import time
from tqdm import tqdm
import matplotlib.pyplot as plt
conn = psycopg2.connect(dbname='PROJEK_KUD2.0', user='postgres', password='2', host='localhost', port=5432) 
cur = conn.cursor() 


# LOADING
def loading():
    for i in tqdm(range(100), desc="Loading", ascii=False, ncols=75, colour="green", unit="", bar_format="{l_bar}{bar}"):
        time.sleep(0.01)
    time.sleep(1)
    
# REGISTER
def register(cur):
    os.system('cls')
    panjang_border = 50 
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "REGISTER".center(panjang_border))
    print("[bold red]" + "=" * 50)
    print("Silahkan Register Terlebih Dahulu")
    nama_customer = input("Masukkan Nama: ")
    no_telp = input("Masukkan No Telepon: ")
    username = input("Masukkan Username: ")
    query_select = "SELECT * FROM customer"
    cur.execute(query_select)
    data = cur.fetchall()
    for customer in data:
        if customer[3] == username:
            print("Username sudah digunakan")
            register(cur)
    password = input("Masukkan Password: ")
    for i in nama_customer:
        if i == "1" or i == "2" or i == "3" or i == "4" or i == "5" or i == "6" or i == "7" or i == "8" or i == "9" or i == "0":
            print("[bold red]" + "\u26A0 Error :" + "[white]" + " Nama tidak boleh mengandung angka")  
            loading()
            register(cur)
    query_register = "INSERT INTO customer (nama_customer, no_telp, username, password) VALUES (%s, %s, %s, %s)"
    cur.execute(query_register, (nama_customer, no_telp, username, password)) #Menyiapkan query SQL untuk memasukkan data pengguna ke dalam tabel Customer
    conn.commit()
    print("Register Berhasil")
    loading()
    login(cur)
    
# LOGIN
def login(cur):
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "LOGIN".center(panjang_border))
    print("[bold red]" + "=" * 50)
    print("Silahkan Login Terlebih Dahulu")
    username = input("Masukkan Username: ")
    password = input("Masukkan Password: ")
    query_login = f"SELECT * FROM customer WHERE username = '{username}' AND password = '{password}'"
    cur.execute(query_login, (username, password))
    data = cur.fetchall()
    if data:
        print("Login Berhasil")
        loading()
        menu_customer(cur)
    elif not data:
        query = f"SELECT * FROM karyawan WHERE username = '{username}' AND password = '{password}'"
        cur.execute(query)
        data_karyawan = cur.fetchone()
        if not data_karyawan:
            print("Username atau Password Salah")
            input("Tekan Enter untuk kembali ke login")
            loading()
            login(cur)
        elif data_karyawan[5] == "owner" :
                print("Login Berhasil")
                loading()
                menu_owner(cur)
        elif data_karyawan[5] == "karyawan" :
                print("Login Berhasil")
                loading()
                menu_karyawan(cur)
        else:
            print("Login Gagal")
            menu_awal()
    else:
        print("Login Gagal")
        print("Username atau Password Salah")
        login(cur)
    cur.close() 
    conn.close()
    
# MENU PRODUK 
def menu_produk_main(cur): 
    os.system('cls') 
    panjang_border = 50  
    print("[bold red]" + "=" * panjang_border) 
    print("[bold cyan]" + "MENU PRODUK".center(panjang_border)) 
    print("[bold red]" + "=" * panjang_border) 
    print("1. Tambah Produk") 
    print("2. Lihat Produk") 
    print("3. Sorting Produk")
    print("4. Update Produk") 
    print("5. Hapus Produk") 
    print("6. Kembali") 
    pilihan = input("Masukkan pilihan: ") 
    if pilihan == "1": 
        tambah_data_produk(cur) 
    elif pilihan == "2": 
        lihat_data_produk(cur) 
    elif pilihan == "3": 
        sorting_data_produk(cur)    
    elif pilihan == "4": 
        update_data_produk(cur)
    elif pilihan == "5":
        hapus_data_produk(cur)
    elif pilihan == "6":
        menu_karyawan(cur)
    else:
        print("Pilihan tidak ada")
        menu_karyawan(cur)

# Fitur Tambah Data Produk
def tambah_data_produk(cur):
    panjang_border = 50
    print("[bold red]" + "=" * panjang_border)
    print("[bold cyan]" + "MENU PRODUK".center(panjang_border))
    print("[bold cyan]" + "FITUR TAMBAH DATA PRODUK".center(panjang_border))
    print("[bold red]" + "=" * panjang_border)
    nama_produk = input("Masukkan nama produk: ")
    harga_produk = int(input("Masukkan harga produk: "))
    stok_produk = int(input("Masukkan stok produk: "))
    jenis = input("Masukkan jenis produk: ")
    expired_date = input("Masukkan expired date produk(YYYY-MM-DD): ")
    query_tambah = "INSERT INTO produk (nama_produk, harga_produk, stok_produk, jenis, exp_date) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(query_tambah, (nama_produk, harga_produk, stok_produk, jenis, expired_date))
    conn.commit()
    print("Produk berhasil ditambahkan")
    input("Tekan enter untuk kembali ke menu produk")
    menu_produk_main(cur)
    cur.close()
    conn.close()

# Fitur Lihat Data Produk   
def lihat_data_produk(cur):
    os.system("cls")
    panjang_border = 70
    print("[bold red]" + "=" * panjang_border)
    print("[bold cyan]" + "MENU PRODUK".center(panjang_border))
    print("[bold cyan]" + "FITUR LIHAT DATA PRODUK".center(panjang_border))
    print("[bold red]" + "=" * panjang_border)
    query_lihat = "SELECT * FROM produk order by id_produk"
    cur.execute(query_lihat)
    data = cur.fetchall()
    print(tabulate.tabulate(data, headers=["ID", "Nama Produk", "Harga Produk", "Stok Produk", "Jenis", "Expired Date"]))
    cari_data = input("Apakah ingin mencari data? (y/n): ")
    if cari_data == "y":
        nama_produk = input("Masukkan nama produk yang ingin dicari(huruf depan wajib kapital): ")
        data_ditemukan = []
        for produk in data:
            if nama_produk in produk[1]:
                data_ditemukan.append(produk)
        if not data_ditemukan:
            print("Data tidak ditemukan")
        else:
            print(tabulate.tabulate(data_ditemukan, headers=["ID", "Nama Produk", "Harga Produk", "Stok Produk"]))
        input("Tekan enter untuk kembali ke menu produk")
        menu_produk_main(cur)
    else:
        input("Tekan enter untuk kembali ke menu produk")
        menu_produk_main(cur)
    cur.close()
    conn.close()
    
# Sorting Data Produk  
def partition(array, left, right, key_index):
    pivot = array[right][key_index]
    i = left - 1
    for j in range(left, right):
        if array[j][key_index] <= pivot:
            i = i + 1
            array[i], array[j] = array[j], array[i]
    array[i + 1], array[right] = array[right], array[i + 1]
    return i + 1

def quicksort(array, left, right, key_index):
    if left < right:
        pivotIndex = partition(array, left, right, key_index)
        quicksort(array, left, pivotIndex - 1, key_index)
        quicksort(array, pivotIndex + 1, right, key_index)
    
def sorting_data_produk(cur):
    query = f"SELECT * FROM produk"
    cur.execute(query)
    data = cur.fetchall()
    key_index = 1
    quicksort(data, 0, len(data) - 1, key_index)
    for row in data:
        print(row)
    
    input("Tekan enter untuk kembali ke menu produk")
    menu_produk_main(cur)
        
def update_data_produk(cur):
    os.system("cls")
    panjang_border = 50
    print("[bold red]" + "=" * panjang_border)
    print("[bold cyan]" + "MENU PRODUK".center(panjang_border))
    print("[bold cyan]" + "FITUR UPDATE DATA PRODUK".center(panjang_border))
    print("[bold red]" + "=" * panjang_border)
    query_lihat = "SELECT * FROM produk order by id_produk "
    cur.execute(query_lihat)
    data = cur.fetchall()
    print(tabulate.tabulate(data, headers=["ID", "Nama Produk", "Harga Produk", "Stok Produk", "Jenis", "Expired Date"]))
    id_produk = input("Masukkan ID produk yang ingin diupdate: ")
    query_pilih = "SELECT * FROM produk WHERE id_produk = %s"
    cur.execute(query_pilih, (id_produk,))
    data_pilih = cur.fetchone()
    print("Data yang ingin diupdate: ")
    print("ID: ", data_pilih[0])
    print("Nama Produk: ", data_pilih[1])
    print("Harga Produk: ", data_pilih[2])
    print("Stok Produk: ", data_pilih[3])
    nama_produk = input("Masukkan nama produk baru: ") or data_pilih[1]
    harga_produk = input("Masukkan harga produk baru: ") or data_pilih[2]
    harga_produk = int(harga_produk)
    stok_produk = input("Masukkan stok produk baru: ") or data_pilih[3]
    stok_produk = int(stok_produk)
    query_update = "UPDATE produk SET nama_produk = %s, harga_produk = %s, stok_produk = %s WHERE id_produk = %s"
    cur.execute(query_update, (nama_produk, harga_produk, stok_produk, id_produk))
    conn.commit()
    print("Produk berhasil diupdate")
    input("Tekan enter untuk kembali ke menu produk")
    menu_produk_main(cur)
    cur.close()
    conn.close()
    
def hapus_data_produk(cur):
    os.system("cls")
    panjang_border = 70
    print("[bold red]" + "=" * panjang_border)
    print("[bold cyan]" + "MENU PRODUK".center(panjang_border))
    print("[bold cyan]" + "FITUR HAPUS DATA PRODUK".center(panjang_border))
    print("[bold red]" + "=" * panjang_border)
    query_lihat = "SELECT * FROM produk order by id_produk"
    cur.execute(query_lihat)
    data = cur.fetchall()
    print(tabulate.tabulate(data, headers=["ID", "Nama Produk", "Harga Produk", "Stok Produk"]))
    id_produk = input("Masukkan ID produk yang ingin dihapus: ")
    query_hapus = "DELETE FROM produk WHERE id_produk = %s"
    cur.execute(query_hapus, (id_produk,))
    conn.commit()
    print("Produk berhasil dihapus")
    input("Tekan enter untuk kembali ke menu produk")
    menu_produk_main(cur)
    cur.close()
    conn.close()
    
def menu_karyawan_main(cur):
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "DATA KARYAWAN".center(panjang_border))
    print("[bold red]" + "=" * 50)
    print("1. Tambah Data Karyawan")
    print("2. Lihat Data Karyawan")
    print("3. Update Data Karyawan")
    print("4. Hapus Data Karyawan")
    print("5. Kembali")
    pilihan = input("Masukkan pilihan: ")
    if pilihan == "1":
        tambah_data_karyawan(cur)
    elif pilihan == "2":
        lihat_data_karyawan(cur)
    elif pilihan == "3":
        update_data_karyawan(cur)
    elif pilihan == "4":
        hapus_data_karyawan(cur)
    elif pilihan == "5":
        menu_owner(cur)
        
def tambah_data_karyawan(cur):
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "TAMBAH DATA KARYAWAN".center(panjang_border))
    print("[bold red]" + "=" * 50)
    query = "SELECT * FROM karyawan"
    cur.execute(query)
    data = cur.fetchall()
    id = len(data) + 1
    id = int(id)
    nama_karyawan = input("Masukkan nama karyawan: ")
    no_telp = input("Masukkan no telepon: ")
    no_telp = str(no_telp)
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")
    role = input("Masukkan jabatan (owner/karyawan): ")
    query_tambah = "INSERT INTO karyawan (id_karyawan, nama_karyawan, no_telp, username, password, nama_jabatan) VALUES (%s,%s, %s, %s, %s, %s)"
    cur.execute(query_tambah, (id, nama_karyawan, no_telp, username, password, role))
    conn.commit()
    print("Data karyawan berhasil ditambahkan")
    input("Tekan enter untuk kembali ke menu karyawan")
    menu_karyawan_main(cur)
    
def lihat_data_karyawan(cur):
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "LIHAT DATA KARYAWAN".center(panjang_border))
    print("[bold red]" + "=" * 50)
    query_lihat = "SELECT * FROM karyawan order by id_karyawan"
    cur.execute(query_lihat)
    data = cur.fetchall()
    print(tabulate.tabulate(data, headers=["ID", "Nama Karyawan", "No Telepon", "Username", "Password", "Role"]))
    input("Tekan enter untuk kembali ke menu karyawan")
    menu_karyawan_main(cur)
    
def update_data_karyawan(cur):
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "UPDATE DATA KARYAWAN".center(panjang_border))
    print("[bold red]" + "=" * 50)
    query_lihat = "SELECT * FROM karyawan order by id_karyawan"
    cur.execute(query_lihat)
    data = cur.fetchall()
    print(tabulate.tabulate(data, headers=["ID", "Nama Karyawan", "No Telepon", "Username", "Password", "Role"]))
    id_karyawan = input("Masukkan ID karyawan yang ingin diupdate: ")
    query_pilih = "SELECT * FROM karyawan WHERE id_karyawan = %s"
    cur.execute(query_pilih, (id_karyawan,))
    data_pilih = cur.fetchone()
    print("Data yang ingin diupdate: ")
    print("ID: ", data_pilih[0])
    print("Nama Karyawan: ", data_pilih[1])
    print("No Telepon: ", data_pilih[2])
    print("Username: ", data_pilih[3])
    print("Password: ", data_pilih[4])
    print("Role: ", data_pilih[5])
    nama_karyawan = input("Masukkan nama karyawan baru: ") or data_pilih[1]
    no_telp = input("Masukkan no telepon baru: ") or data_pilih[2]
    username = input("Masukkan username baru: ") or data_pilih[3]
    password = input("Masukkan password baru: ") or data_pilih[4]
    role = input("Masukkan jabatan baru: ") or data_pilih[5]
    query_update = "UPDATE karyawan SET nama_karyawan = %s, no_telp = %s, username = %s, password = %s, nama_jabatan = %s WHERE id_karyawan = %s"
    cur.execute(query_update, (nama_karyawan, no_telp, username, password, role, id_karyawan))
    conn.commit()
    print("Data karyawan berhasil diupdate")
    input("Tekan enter untuk kembali ke menu karyawan")
    menu_karyawan_main(cur)
    
def hapus_data_karyawan(cur):
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "HAPUS DATA KARYAWAN".center(panjang_border))
    print("[bold red]" + "=" * 50)
    query_lihat = "SELECT * FROM karyawan order by id_karyawan"
    cur.execute(query_lihat)
    data = cur.fetchall()
    print(tabulate.tabulate(data, headers=["ID", "Nama Karyawan", "No Telepon", "Username", "Password", "Role"]))
    id_karyawan = input("Masukkan ID karyawan yang ingin dihapus: ")
    query_hapus = "DELETE FROM karyawan WHERE id_karyawan = %s"
    cur.execute(query_hapus, (id_karyawan,))
    conn.commit()
    print("Data karyawan berhasil dihapus")
    input("Tekan enter untuk kembali ke menu karyawan")
    menu_karyawan_main(cur)
           
# MENU TRANSAKSI KARYAWAN
def riwayat_transaksi_karyawan(cur, caller):
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "RIWAYAT TRANSAKSI".center(panjang_border))
    print("[bold red]" + "=" * 50)
    print("1. Lihat Riwayat Transaksi Pembelian")
    print("2. Lihat Riwayat Transaksi Penjualan")
    print("3. Kembali")
    pilih = input("Pilih Menu: ")
    if pilih == "1":
        riwayat_transaksi_pembelian_karyawan(cur, caller)
    elif pilih == "2":
        riwayat_transaksi_penjualan_karyawan(cur, caller)
    elif pilih == "3":
        if caller == "karyawan":
            menu_karyawan(cur)
        elif caller == "owner":
            menu_owner(cur)
    else:
        print("Menu Tidak Ada")
        riwayat_transaksi_karyawan(caller)

# FITUR RIWAYAT TRANSAKSI PEMBELIAN KARYAWAN
def riwayat_transaksi_pembelian_karyawan(cur, caller):
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "RIWAYAT TRANSAKSI PEMBELIAN".center(panjang_border))
    print("[bold red]" + "=" * 50)
    query_riwayat_pembelian = "SELECT * FROM riwayat_pembelian order by id_riwayat_pembelian"
    cur.execute(query_riwayat_pembelian)
    data = cur.fetchall()
    print(tabulate.tabulate(data, headers=["ID", "Customer", "Tanggal Pembelian", "ID Produk", "Kuantitas", "Sub Total"]))
    print("Mau mencari data? (y/n)")
    cari_data = input("Masukkan pilihan: ")
    if cari_data == "y":
        nama_customer = input("Masukkan nama customer: ")
        data_ditemukan = []
        for pembelian in data:
            if nama_customer in pembelian[1]:
                data_ditemukan.append(pembelian)
        if not data_ditemukan:
            print("Data tidak ditemukan")
        else:
            print(tabulate.tabulate(data_ditemukan, headers=["ID", "Customer", "Tanggal Pembelian", "ID Produk", "Kuantitas", "Sub Total"]))
        input("Tekan enter untuk kembali ke menu riwayat transaksi")
        if caller == "karyawan":
            riwayat_transaksi_karyawan(cur, caller)
        elif caller == "owner":
            riwayat_transaksi_karyawan(cur, caller)
    else:
        input("Tekan enter untuk kembali ke menu riwayat transaksi")
        if caller == "karyawan":
            riwayat_transaksi_karyawan(cur, caller)
        elif caller == "owner":
            riwayat_transaksi_karyawan(cur, caller)
    cur.close()
    conn.close()

# FITUR RIWAYAT TRANSAKSI PENJUALAN KARYAWAN 
def riwayat_transaksi_penjualan_karyawan(cur, caller):
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "RIWAYAT TRANSAKSI PENJUALAN".center(panjang_border))
    print("[bold red]" + "=" * 50)
    query_riwayat_penjualan = "SELECT * FROM riwayat_penjualan order by id_riwayat_penjualan"
    cur.execute(query_riwayat_penjualan)
    data = cur.fetchall()
    print(tabulate.tabulate(data, headers=["ID", "Customer", "Tanggal Penjualan", "ID Produk", "Kuantitas", "Sub Total"]))
    print("Mau mencari data? (y/n)")
    cari_data = input("Masukkan pilihan: ")
    if cari_data == "y":
        nama_customer = input("Masukkan nama customer: ")
        data_ditemukan = []
        for penjualan in data:
            if nama_customer in penjualan[1]:
                data_ditemukan.append(penjualan)
        if not data_ditemukan:
            print("Data tidak ditemukan")
        else:
            print(tabulate.tabulate(data_ditemukan, headers=["ID", "Customer", "Tanggal Penjualan", "ID Produk", "Kuantitas", "Sub Total"]))
        input("Tekan enter untuk kembali ke menu riwayat transaksi")
        if caller == "karyawan":
            riwayat_transaksi_karyawan(cur, caller)
        elif caller == "owner":
            riwayat_transaksi_karyawan(cur, caller)
    else:
        input("Tekan enter untuk kembali ke menu riwayat transaksi")
        if caller == "karyawan":
            riwayat_transaksi_karyawan(cur, caller)
        elif caller == "owner":
            riwayat_transaksi_karyawan(cur, caller)
    cur.close()
    conn.close()
    
# MENU TRANSAKSI CUSTOMER
def riwayat_transaksi_cust():
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "RIWAYAT TRANSAKSI".center(panjang_border))
    print("[bold red]" + "=" * 50)
    print("1. Lihat Riwayat Transaksi Pembelian")
    print("2. Lihat Riwayat Transaksi Penjualan")
    print("3. Kembali")
    pilih = input("Pilih Menu: ")
    if pilih == "1":
        riwayat_transaksi_pembelian(cur)
    elif pilih == "2":
        riwayat_transaksi_penjualan(cur)
    elif pilih == "3":
        menu_customer(cur)
    else:
        print("Menu Tidak Ada")
        riwayat_transaksi_cust()

# FITUR RIWAYAT TRANSAKSI PEMBELIAN CUSTOMER
def riwayat_transaksi_pembelian(cur):
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "RIWAYAT TRANSAKSI PEMBELIAN".center(panjang_border))
    print("[bold red]" + "=" * 50)
    nama_customer = input("Masukkan nama customer: ")
    query_riwayat_pembelian = "SELECT * FROM riwayat_pembelian WHERE customer = %s order by id_riwayat_pembelian"
    cur.execute(query_riwayat_pembelian, (nama_customer,))
    data = cur.fetchall()
    print(tabulate.tabulate(data, headers=["ID", "Customer", "Tanggal Pembelian", "ID Produk", "Kuantitas", "Sub Total"]))
    print("Mau mencari data? (y/n)")
    cari_data = input("Masukkan pilihan: ")
    if cari_data == "y":
        nama_customer = input("Masukkan nama customer: ")
        data_ditemukan = []
        for pembelian in data:
            if nama_customer in pembelian[1]:
                data_ditemukan.append(pembelian)
        if not data_ditemukan:
            print("Data tidak ditemukan")
        else:
            print(tabulate.tabulate(data_ditemukan, headers=["ID", "Customer", "Tanggal Pembelian", "ID Produk", "Kuantitas", "Sub Total"]))
        input("Tekan enter untuk kembali ke menu riwayat transaksi")
        riwayat_transaksi_cust()
    else:
        input("Tekan enter untuk kembali ke menu riwayat transaksi")
        riwayat_transaksi_cust()
    cur.close()
    conn.close()

# FITUR RIWAYAT TRANSAKSI PENJUALAN CUSTOMER 
def riwayat_transaksi_penjualan(cur):
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "RIWAYAT TRANSAKSI PENJUALAN".center(panjang_border))
    print("[bold red]" + "=" * 50)
    query_riwayat_penjualan = "SELECT * FROM riwayat_penjualan order by id_riwayat_penjualan"
    cur.execute(query_riwayat_penjualan)
    data = cur.fetchall()
    print(tabulate.tabulate(data, headers=["ID", "Customer", "Tanggal Penjualan", "ID Produk", "Kuantitas", "Sub Total"]))
    print("Mau mencari data? (y/n)")
    cari_data = input("Masukkan pilihan: ")
    if cari_data == "y":
        nama_customer = input("Masukkan nama customer: ")
        data_ditemukan = []
        for penjualan in data:
            if nama_customer in penjualan[1]:
                data_ditemukan.append(penjualan)
        if not data_ditemukan:
            print("Data tidak ditemukan")
        else:
            print(tabulate.tabulate(data_ditemukan, headers=["ID", "Customer", "Tanggal Penjualan", "ID Produk", "Kuantitas", "Sub Total"]))
        input("Tekan enter untuk kembali ke menu riwayat transaksi")
        riwayat_transaksi_cust()
    else:
        input("Tekan enter untuk kembali ke menu riwayat transaksi")
        riwayat_transaksi_cust()
    cur.close()
    conn.close()
    
# MENU LAPORAN PENJUALAN
def menu_laporan_penjualan(cur, caller):
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "MENU LAPORAN PENJUALAN".center(panjang_border))
    print("[bold red]" + "=" * 50)
    bulan = input("Masukkan bulan: ")
    query_laporan = "SELECT * FROM laporan_penjualan WHERE bulan = %s"
    cur.execute(query_laporan, (bulan,))
    data = cur.fetchall()
    print(tabulate.tabulate(data, headers=["ID", "Bulan", "Tahun", "Nama Produk", "Total Penjualan", "Total Stok"]))
    tampilan_grafik = input("Mau tampilkan grafik? (y/n): ")
    if tampilan_grafik == "y":
        query = "SELECT * FROM laporan_penjualan WHERE bulan = %s"
        cur.execute(query, (bulan,))
        data = cur.fetchall()
        nama_produk = []
        total_penjualan = []
        total_stok = []
        
        for produk in data:
            nama_produk.append(produk[3])
            total_penjualan.append(produk[4])
            total_stok.append(produk[5])
            
        fig, axs = plt.subplots(1, 2, figsize =(5, 8), tight_layout = True)

        bar1 = axs[0].bar(nama_produk, total_penjualan, color = 'b')
        bar2 = axs[1].bar(nama_produk, total_stok, color = 'r')
        
        axs[0].set_title('Total Penjualan')
        axs[1].set_title('Total Stok')

        def autolabel(ax, bars):
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2., height,
                        '%d' % int(height),
                        ha='center', va='bottom')

        autolabel(axs[0], bar1)
        autolabel(axs[1], bar2)

        plt.show()
        input("Tekan enter untuk kembali ke menu laporan")
        if caller == "karyawan":
            menu_karyawan(cur)
        elif caller == "owner":
            menu_owner(cur)
    else:
        input("Tekan enter untuk kembali ke menu laporan")
        if caller == "karyawan":
            menu_karyawan(cur)
        elif caller == "owner":
            menu_owner(cur)
    cur.close()
    conn.close()
    
# MENU LAPORAN PEMBELIAN
def menu_laporan_pembelian(cur, caller):
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "MENU LAPORAN PEMBELIAN".center(panjang_border))
    print("[bold red]" + "=" * 50)
    bulan = input("Masukkan bulan: ")
    query_laporan = "SELECT * FROM laporan_pembelian WHERE bulan = %s"
    cur.execute(query_laporan, (bulan,))
    data = cur.fetchall()
    print(tabulate.tabulate(data, headers=["ID", "Bulan", "Tahun", "Nama Produk", "Total Pembelian", "Total Stok"]))
    tampilan_grafik = input("Mau tampilkan grafik? (y/n): ")
    if tampilan_grafik == "y":
        query = "SELECT * FROM laporan_pembelian WHERE bulan = %s"
        cur.execute(query, (bulan,))
        data = cur.fetchall()
        nama_produk = []
        total_pembelian = []
        total_stok = []
        
        for produk in data:
            nama_produk.append(produk[3])
            total_pembelian.append(produk[4])
            total_stok.append(produk[5])
            
        fig, axs = plt.subplots(1, 2, figsize =(5, 8), tight_layout = True)

        bar1 = axs[0].bar(nama_produk, total_pembelian, color = 'b')
        bar2 = axs[1].bar(nama_produk, total_stok, color = 'r')
        
        axs[0].set_title('Total Pembelian')
        axs[1].set_title('Total Stok')

        def autolabel(ax, bars):
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2., height,
                        '%d' % int(height),
                        ha='center', va='bottom')

        autolabel(axs[0], bar1)
        autolabel(axs[1], bar2)

        plt.show()
        input("Tekan enter untuk kembali ke menu laporan")
        if caller == "karyawan":
            menu_karyawan(cur)
        elif caller == "owner":
            menu_owner(cur)
    else:
        input("Tekan enter untuk kembali ke menu laporan")
        if caller == "karyawan":
            menu_karyawan(cur)
        elif caller == "owner":
            menu_owner(cur)
    cur.close()
    conn.close()
    
# Fitur Expired Date
def expired_date(cur, caller):
    os.system('cls')
    panjang_border = 80
    print("[bold red]" + "=" * 80)
    print("[bold cyan]" + "CEK EXPIRED DATE".center(panjang_border))
    print("[bold red]" + "=" * 80)
    query_select = "SELECT * FROM produk"
    cur.execute(query_select)
    data = cur.fetchall()

    data_expired = []
    for produk in data:
        if produk[5] == datetime.date.today():
            data_expired.append(produk)
    if not data_expired:
        data_expired.append(["Tidak ada", "Tidak ada", "Tidak ada","Tidak ada","Tidak ada","Tidak ada"])
    print(tabulate.tabulate(data_expired, headers=["ID", "Nama Produk", "Harga Produk", "Stok Produk", "Jenis", "Expired Date"]))
    input("Tekan enter untuk kembali ke menu produk")
    if caller == "karyawan":
        menu_karyawan(cur)
    elif caller == "owner":
        menu_owner(cur)
    cur.close()
    conn.close()
    
# Fitur Reminder Stok
def reminder_stok(cur, caller):
    os.system('cls')
    panjang_border = 80
    print("[bold red]" + "=" * 80)
    print("[bold cyan]" + "CEK STOK".center(panjang_border))
    print("[bold red]" + "=" * 80)
    query_select = "SELECT * FROM produk"
    cur.execute(query_select)
    data = cur.fetchall()

    data_stok = []
    for produk in data:
        if produk[3] <= 5:
            data_stok.append(produk)
    if not data_stok:
        data_stok.append(["Tidak ada", "Tidak ada", "Tidak ada","Tidak ada","Tidak ada","Tidak ada"])
    print(tabulate.tabulate(data_stok, headers=["ID", "Nama Produk", "Harga Produk", "Stok Produk", "Jenis", "Expired Date"]))
    input("Tekan enter untuk kembali ke menu produk")
    if caller == "karyawan":
        menu_karyawan(cur)
    elif caller == "owner":
        menu_owner(cur)
    cur.close()
    conn.close()
    
# Fitur Beli Produk
def beli_produk(cur):
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "BELI PRODUK".center(panjang_border))
    print("[bold red]" + "=" * 50)
    nama_customer = input("Masukkan nama anda: ")
    query_customer = "SELECT * FROM customer WHERE nama_customer = %s"
    cur.execute(query_customer, (nama_customer,))
    data_customer = cur.fetchone()
    if not data_customer:
        print("Customer tidak ditemukan")
        beli_produk(cur)    
    query_produk = "SELECT * FROM produk"
    cur.execute(query_produk)
    data = cur.fetchall()
    print(tabulate.tabulate(data, headers=["ID", "Nama Produk", "Harga Produk", "Stok Produk", "Jenis", "Expired Date"]))
    nama_produk = input("Masukkan Nama Produk: ")
    cur.execute("SELECT * FROM produk WHERE nama_produk = %s", (nama_produk,))
    tgl_transaksi = datetime.date.today()
    total_stok = input("Masukkan jumlah stok yang ingin dibeli: ")
    total_stok = int(total_stok)
    data_produk = cur.fetchone()
    if data_produk[3] < total_stok:
        print("Stok tidak mencukupi")
        beli_produk(cur)
    else:
        sub_total = total_stok * data_produk[2]
        sub_total = int(sub_total)
        query_beli = "INSERT INTO riwayat_pembelian (customer, tgl_transaksi, nama_produk, total_stok, subtotal) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query_beli, (nama_customer, tgl_transaksi, nama_produk, total_stok, sub_total))
        conn.commit()
        select_stok = "SELECT stok_produk FROM produk WHERE nama_produk = %s"
        cur.execute(select_stok, (nama_produk,))
        stok_produk = cur.fetchone()
        stok_produk = stok_produk[0] - total_stok
        update_stok = "UPDATE produk SET stok_produk = %s WHERE nama_produk = %s"
        cur.execute(update_stok, (stok_produk, nama_produk))
        conn.commit()
        bulan = datetime.date.today().month
        tahun = datetime.date.today().year
        query = "SELECT * FROM laporan_penjualan WHERE nama_produk = %s"
        cur.execute(query, (nama_produk,))
        data_laporan = cur.fetchone()
        if not data_laporan:
            query_laporan = "INSERT INTO laporan_penjualan (bulan, tahun, nama_produk, total_penjualan, total_stok) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(query_laporan, (bulan, tahun, nama_produk, sub_total, total_stok))
            conn.commit()
        elif data_laporan[3] == nama_produk:
            total_penjualan = data_laporan[4] + sub_total
            total_stok = data_laporan[5] + total_stok
            query_laporan = "UPDATE laporan_penjualan SET total_penjualan = %s, total_stok = %s WHERE nama_produk = %s"
            cur.execute(query_laporan, (total_penjualan, total_stok, nama_produk))
            conn.commit()
        print("Transaksi Berhasil")
        input("Tekan enter untuk kembali ke menu customer")
        menu_customer(cur)
        
# Fitur Jual Produk
def jual_produk(cur):
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "JUAL PRODUK".center(panjang_border))
    print("[bold red]" + "=" * 50)
    nama_customer = input("Masukkan nama anda: ")
    nama_produk = input("Masukkan nama produk yang ingin dijual: ")
    query_customer = "SELECT * FROM customer WHERE nama_customer = %s"
    cur.execute(query_customer, (nama_customer,))
    data_customer = cur.fetchone()
    if not data_customer:
        print("Customer tidak ditemukan")
        jual_produk()
    query_produk = "SELECT * FROM produk"
    cur.execute(query_produk)
    data = cur.fetchone()
    if nama_produk not in data:
        tgl_transaksi = datetime.date.today()
        total_stok = input("Masukkan jumlah stok yang ingin dijual: ")
        total_stok = int(total_stok)
        harga = input("Masukkan harga produk: ")
        harga = int(harga)
        sub_total = total_stok * harga
        sub_total = int(sub_total)
        query_jual = "INSERT INTO riwayat_penjualan (customer, tgl_transaksi, nama_produk, total_stok, subtotal) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query_jual, (nama_customer, tgl_transaksi, nama_produk, total_stok, sub_total))
        conn.commit()
        jenis = input("Masukkan jenis produk: ")
        expired_date = input("Masukkan expired date produk (YYYY-MM-DD): ")
        query_produk = "INSERT INTO produk (nama_produk, harga_produk, stok_produk, jenis, exp_date) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query_produk, (nama_produk, harga, total_stok, jenis, expired_date))
        conn.commit()
        bulan = datetime.date.today().month
        tahun = datetime.date.today().year
        query = "SELECT * FROM laporan_pembelian WHERE nama_produk = %s"
        cur.execute(query, (nama_produk,))
        data_laporan = cur.fetchone()
        if not data_laporan:
            query_laporan = "INSERT INTO laporan_pembelian (bulan, tahun, nama_produk, total_pembelian, total_stok) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(query_laporan, (bulan, tahun, nama_produk, sub_total, total_stok))
            conn.commit()
        elif data_laporan[3] == nama_produk:
            total_pembelian = data_laporan[4] + sub_total
            total_stok = data_laporan[5] + total_stok
            query_laporan = "UPDATE laporan_pembelian SET total_pembelian = %s, total_stok = %s WHERE nama_produk = %s"
            cur.execute(query_laporan, (total_pembelian, total_stok, nama_produk))
            conn.commit()
        print("Transaksi Berhasil")
        input("Tekan enter untuk kembali ke menu customer")
        menu_customer(cur)
    elif nama_produk in data:
        tgl_transaksi = datetime.date.today()
        total_stok = input("Masukkan jumlah stok yang ingin dijual: ")
        total_stok = int(total_stok)
        harga = input("Masukkan harga produk: ")
        harga = int(harga)
        sub_total = total_stok * harga
        sub_total = int(sub_total)
        query_jual = "INSERT INTO riwayat_penjualan (customer, tgl_transaksi, nama_produk, total_stok, subtotal) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query_jual, (nama_customer, tgl_transaksi, nama_produk, total_stok, sub_total))
        conn.commit()
        bulan = datetime.date.today().month
        tahun = datetime.date.today().year
        query = "SELECT * FROM laporan_pembelian WHERE nama_produk = %s"
        cur.execute(query, (nama_produk,))
        data_laporan = cur.fetchone()
        if not data_laporan:
            query_laporan = "INSERT INTO laporan_pembelian (bulan, tahun, nama_produk, total_pembelian, total_stok) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(query_laporan, (bulan, tahun, nama_produk, sub_total, total_stok))
            conn.commit()
        elif data_laporan[3] == nama_produk:
            total_pembelian = data_laporan[4] + sub_total
            total_stok = data_laporan[5] + total_stok
            query_laporan = "UPDATE laporan_pembelian SET total_pembelian = %s, total_stok = %s WHERE nama_produk = %s"
            cur.execute(query_laporan, (total_pembelian, total_stok, nama_produk))
            conn.commit()
        select_stok = "SELECT stok_produk FROM produk WHERE nama_produk = %s"
        cur.execute(select_stok, (nama_produk,))
        stok_produk = cur.fetchone()
        stok_produk = stok_produk[0] + total_stok
        update_stok = "UPDATE produk SET stok_produk = %s WHERE nama_produk = %s"
        cur.execute(update_stok, (stok_produk, nama_produk))
        conn.commit()
        print("Transaksi Berhasil")
        input("Tekan enter untuk kembali ke menu customer")
        menu_customer(cur)
    else:
        print("Produk tidak ditemukan")
        jual_produk()
        
# MENU CUSTOMER
def menu_customer(cur):
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "MENU CUSTOMER".center(panjang_border))
    print("[bold red]" + "=" * 50)
    print("1. Lihat Produk")
    print("2. Beli Produk")
    print("3. Jual Produk")
    print("4. Lihat Riwayat Transaksi")
    print("5. Kembali")
    pilihan = input("Masukkan pilihan: ")
    if pilihan == "1":
        os.system("cls")
        panjang_border = 70
        print("[bold red]" + "=" * panjang_border)
        print("[bold cyan]" + "MENU CUSTOMER".center(panjang_border))
        print("[bold cyan]" + "FITUR LIHAT DATA PRODUK".center(panjang_border))
        print("[bold red]" + "=" * panjang_border)
        query_lihat = "SELECT * FROM produk order by id_produk"
        cur.execute(query_lihat)
        data = cur.fetchall()
        print(tabulate.tabulate(data, headers=["ID", "Nama Produk", "Harga Produk", "Stok Produk", "Jenis", "Expired Date"]))
        cari_data = input("Apakah ingin mencari data? (y/n): ")
        if cari_data == "y":
            nama_produk = input("Masukkan nama produk yang ingin dicari(huruf depan wajib kapital): ")
            data_ditemukan = []
            for produk in data:
                if nama_produk in produk[1]:
                    data_ditemukan.append(produk)
            if not data_ditemukan:
                print("Data tidak ditemukan")
            else:
                print(tabulate.tabulate(data_ditemukan, headers=["ID", "Nama Produk", "Harga Produk", "Stok Produk"]))
            input("Tekan enter untuk kembali ke menu produk")
            menu_customer(cur)
        else:
            input("Tekan enter untuk kembali ke menu produk")
            menu_customer(cur)
        cur.close()
        conn.close()
    elif pilihan == "2":
        beli_produk(cur)
    elif pilihan == "3":
        jual_produk(cur)
    elif pilihan == "4":
        riwayat_transaksi_cust()
    elif pilihan == "5":
        menu_awal()
    else:
        print("Pilihan tidak ada")
        menu_customer()

# MENU OWNER
def menu_owner(cur):
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "MENU OWNER".center(panjang_border))
    print("[bold red]" + "=" * 50)
    query_select = "SELECT * FROM produk"
    cur.execute(query_select)
    data = cur.fetchall()
    expired_today = False
    low_stock = False
    for produk in data:
        if not expired_today and (produk[5] == datetime.date.today() and produk[5] <= datetime.date.today()):
            print("[bold red]" + "\u26A0 Peringatan :" + "[white]" + " Ada produk yang expired hari ini")
            expired_today = True
        if not low_stock and produk[3] <= 5:
            print("[bold red]" + "\u26A0 Peringatan :" + "[white]" + " Ada produk yang stoknya kurang dari 5")
            low_stock = True
        if expired_today and low_stock:
            break
    if not expired_today:
        print("[bold green]" + "\u2705 Reminder :" + "[white]" + " Tidak ada produk yang expired hari ini")
    if not low_stock:
        print("[bold green]" + "\u2705 Reminder :" + "[white]" + " Tidak ada produk yang stoknya kurang dari 5")
    print("1. Data Karyawan")
    print("2. Riwayat Transaksi")
    print("3. Laporan Penjualan")
    print("4. Laporan Pembelian")
    print("5. Cek Expired Date")
    print("6. Cek Reminder Stok")
    print("7. Kembali")
    pilihan = input("Masukkan pilihan: ")
    if pilihan == "1":
        menu_karyawan_main(cur)
    elif pilihan == "2":
        riwayat_transaksi_karyawan(cur, caller="owner")
    elif pilihan == "3":
        menu_laporan_penjualan(cur, caller="owner")
    elif pilihan == "4":
        menu_laporan_pembelian(cur, caller="owner")
    elif pilihan == "5":
        expired_date(cur, caller="owner")
    elif pilihan == "6":
        reminder_stok(cur, caller="owner")
    elif pilihan == "7":
        menu_awal()
    else:
        print("Pilihan tidak ada")
        menu_karyawan()
        
# MENU KARYAWAN
def menu_karyawan(cur):
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print("[bold cyan]" + "MENU KARYAWAN".center(panjang_border))
    print("[bold red]" + "=" * 50)
    query_select = "SELECT * FROM produk"
    cur.execute(query_select)
    data = cur.fetchall()
    expired_today = False
    low_stock = False
    for produk in data:
        if not expired_today and (produk[5] == datetime.date.today() and produk[5] <= datetime.date.today()):
            print("[bold red]" + "\u26A0 Peringatan :" + "[white]" + " Ada produk yang expired hari ini")
            expired_today = True
        if not low_stock and produk[3] <= 5:
            print("[bold red]" + "\u26A0 Peringatan :" + "[white]" + " Ada produk yang stoknya kurang dari 5")
            low_stock = True
        if expired_today and low_stock:
            break
    if not expired_today:
        print("[bold green]" + "\u2705 Reminder :" + "[white]" + " Tidak ada produk yang expired hari ini")
    if not low_stock:
        print("[bold green]" + "\u2705 Reminder :" + "[white]" + " Tidak ada produk yang stoknya kurang dari 5")
    print("1. Menu Produk")
    print("2. Riwayat Transaksi")
    print("3. Laporan Penjualan")
    print("4. Laporan Pembelian")
    print("5. Cek Expired Date")
    print("6. Cek Reminder Stok")
    print("7. Kembali")
    pilihan = input("Masukkan pilihan: ")
    if pilihan == "1":
        menu_produk_main(cur)
    elif pilihan == "2":
        riwayat_transaksi_karyawan(cur, caller="karyawan")
    elif pilihan == "3":
        menu_laporan_penjualan(cur, caller="karyawan")
    elif pilihan == "4":
        menu_laporan_pembelian(cur, caller="karyawan")
    elif pilihan == "5":
        expired_date(cur, caller="karyawan")
    elif pilihan == "6":
        reminder_stok(cur, caller="karyawan")
    elif pilihan == "7":
        menu_awal()
    else:
        print("Pilihan tidak ada")
        menu_karyawan()
        
# MENU AWAL
def menu_awal():
    os.system('cls')
    panjang_border = 50
    print("[bold red]" + "=" * 50)
    print(" [bold cyan]" + "SELAMAT DATANG DI KUD 2.0".center(panjang_border))
    print("[bold red]" + "=" * 50)
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    pilih = int(input("Pilih Menu: "))
    if pilih == 1:
        register(cur)
    elif pilih == 2:
        login(cur)
    elif pilih == 3:
        print("Terima Kasih")
        exit()
    else:
        print("Menu Tidak Ada")
        menu_awal(cur)
        
menu_awal()