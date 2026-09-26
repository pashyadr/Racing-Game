# Import library Pygame, Time (untuk jeda), dan Random (untuk posisi acak)
import pygame
import time
import random

# Inisialisasi Pygame: wajib dipanggil di awal untuk menjalankan semua modul Pygame
pygame.init()

# --- Konfigurasi Layar Game ---
display_width = 800
display_height = 600

# Pengaturan Batas Jalan (Aspal)
ROAD_LEFT = 100
ROAD_RIGHT = 700
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT

# Membuat objek display/layar dengan ukuran yang sudah ditentukan
gameDisplay = pygame.display.set_mode((display_width, display_height))
# Menentukan judul jendela game
pygame.display.set_caption('Racing Game - Mode Bertahan')

# --- Definisi Warna (RGB) ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
DARK_GRAY = (40, 40, 40)
GREEN = (255, 255, 255)
DARK_GREEN = (0, 100, 0)
BROWN = (50, 50, 50)
LIGHT_GRAY = (80, 80, 80)
LEAF_DARK = (15, 75, 25)      # Bayangan daun
LEAF_MID = (34, 139, 34)      # Warna dasar daun
LEAF_LIGHT = (72, 187, 100)   # Pantulan cahaya daun
LEAF_SHADOW = (20, 70, 20) 
KiNDA_GRAY = (210, 210, 210)   # Bayangan di atas rumput

# --- Parameter Mobil Player dan Musuh ---
# Ukuran Lebar dan Tinggi gambar mobil di layar (Dibiarkan 250x150 agar gambar tidak gepeng)
car_width = 300
car_height = 150

# Membuat objek Clock untuk mengatur frame rate (FPS) game
clock = pygame.time.Clock()

# ==========================================
# BAGIAN LOAD GAMBAR
# ==========================================
try:
    # 1. Load Mobil Player dan mengubah ukurannya sesuai car_width/car_height
    carImg = pygame.image.load('Racer.png')
    carImg = pygame.transform.scale(carImg, (car_width, car_height))

    # 2. Load Mobil Musuh (ukurannya akan di-scale dinamis di fungsi things())
    enemyImg = pygame.image.load('Enemy.png')
except:
    # Fallback: Jika gambar tidak ditemukan, buat kotak biru (player) dan merah (musuh)
    print("WARNING: Gambar 'mobil_keren.png' atau 'musuh.png' gak ketemu!")
    carImg = pygame.Surface((car_width, car_height))
    carImg.fill((0, 0, 255)) # Biru
    enemyImg = pygame.Surface((250, 150))
    enemyImg.fill(RED)       # Merah

# ==========================================

# Fungsi untuk menampilkan skor di pojok kiri atas
def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    # Merender (mengubah) angka skor menjadi objek teks berwarna putih
    text = font.render("Score: " + str(count), True, BLACK)
    # Menempatkan teks di layar pada koordinat (0, 0)
    gameDisplay.blit(text, (0, 0))

# Fungsi untuk menggambar rintangan (musuh)
def things(thingx, thingy, thingw, thingh, color):
    # Mengubah ukuran gambar musuh agar sesuai dengan ukuran rintangan saat ini
    scaled_enemy = pygame.transform.scale(enemyImg, (int(thingw), int(thingh)))
    # Menampilkan gambar musuh di koordinat yang ditentukan
    gameDisplay.blit(scaled_enemy, (thingx, thingy))

# Fungsi untuk menggambar mobil pemain
def car(x, y):
    # Menampilkan gambar mobil pemain (carImg) di koordinat (x, y)
    gameDisplay.blit(carImg, (x, y))

# Fungsi pembantu untuk membuat objek teks (surface dan rect)
def text_objects(text, font):
    # Merender teks menjadi objek Surface (tampilan visual)
    textSurface = font.render(text, True, WHITE)
    # Mendapatkan Rect (kotak pembatas) dari teks
    return textSurface, textSurface.get_rect()

# Fungsi untuk menampilkan pesan besar di tengah layar (misalnya pesan Crash)
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 50)
    # Membuat Surface dan Rect dari teks
    TextSurf, TextRect = text_objects(text, largeText)
    # Menetapkan posisi Rect agar berada di tengah layar
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    # Memperbarui tampilan layar
    pygame.display.update()
    # Memberi jeda 2 detik
    time.sleep(2)
    # Memanggil game_loop() untuk mereset/memulai game baru
    game_loop()

# Fungsi yang dipanggil saat terjadi tabrakan
def crash():
    message_display('Kamu Tabrakan!')

# ==========================================
# FUNGSI MENGGAMBAR LINGKUNGAN JALANAN (RAMAI)
# ==========================================
def draw_environment(track_y):
    # 1. Background Rumput
    gameDisplay.fill(GREEN)

    # 2. Bahu Jalan / Trotoar Abu-abu (Di Luar Aspal)
    shoulder_w = 20
    pygame.draw.rect(gameDisplay, LIGHT_GRAY, (ROAD_LEFT - shoulder_w, 0, shoulder_w, display_height))
    pygame.draw.rect(gameDisplay, LIGHT_GRAY, (ROAD_RIGHT, 0, shoulder_w, display_height))

    # 3. Jalan Aspal Utama
    pygame.draw.rect(gameDisplay, DARK_GRAY, (ROAD_LEFT, 0, ROAD_WIDTH, display_height))

    # 4. Strip Kerb Merah-Putih Presisi (Rapi di Atas Bahu Jalan)
    kerb_h = 40
    for i in range(-2, int(display_height / kerb_h) + 2):
        y_pos = (i * kerb_h) + (track_y % (kerb_h * 2))
        color = RED if (i % 2 == 0) else WHITE
        # Kerb Kiri
        pygame.draw.rect(gameDisplay, color, (ROAD_LEFT - 12, y_pos, 10, kerb_h))
        # Kerb Kanan
        pygame.draw.rect(gameDisplay, color, (ROAD_RIGHT + 2, y_pos, 10, kerb_h))

    # 5. Garis Utuh Putih (Pembatas Aspal & Bahu Jalan) -> Bikin Tampilan Rapi Tegas
    pygame.draw.line(gameDisplay, KiNDA_GRAY, (ROAD_LEFT, 0), (ROAD_LEFT, display_height), 5)
    pygame.draw.line(gameDisplay, KiNDA_GRAY, (ROAD_RIGHT, 0), (ROAD_RIGHT, display_height), 5)

    # 6. Marka Jalan Putus-Putus 3 Lajur (Tengah Jalan)
    dash_h, dash_gap = 50, 30
    total_dash = dash_h + dash_gap
    lane_1_x = ROAD_LEFT + (ROAD_WIDTH / 3)
    lane_2_x = ROAD_LEFT + (ROAD_WIDTH / 3) * 2

    for i in range(-2, int(display_height / total_dash) + 2):
        y_pos = (i * total_dash) + (track_y % total_dash)
        pygame.draw.rect(gameDisplay, WHITE, (lane_1_x - 3, y_pos, 6, dash_h))
        pygame.draw.rect(gameDisplay, WHITE, (lane_2_x - 3, y_pos, 6, dash_h))

    # 7. Pohon Rindang & Bervolume (Di Luar Jalan)
    tree_gap = 180
    for i in range(-2, int(display_height / tree_gap) + 2):
        y_pos = (i * tree_gap) + (track_y % tree_gap)
        
        # Gambar Pohon Kiri & Kanan menggunakan posisi X masing-masing
        for tree_x in [40, 760]:
            # a. Bayangan Pohon di Atas Rumput
            pygame.draw.ellipse(gameDisplay, LEAF_SHADOW, (tree_x - 22, y_pos + 12, 44, 14))

            # b. Batang Pohon
            pygame.draw.rect(gameDisplay, BROWN, (tree_x - 4, y_pos - 5, 8, 20))

            # c. Dedaunan Berlapis (Gelap / Belakang)
            pygame.draw.circle(gameDisplay, LEAF_DARK, (tree_x - 12, y_pos - 10), 14)
            pygame.draw.circle(gameDisplay, LEAF_DARK, (tree_x + 12, y_pos - 10), 14)
            pygame.draw.circle(gameDisplay, LEAF_DARK, (tree_x, y_pos - 24), 16)

            # d. Dedaunan Berlapis (Warna Utama / Tengah)
            pygame.draw.circle(gameDisplay, LEAF_MID, (tree_x - 8, y_pos - 12), 12)
            pygame.draw.circle(gameDisplay, LEAF_MID, (tree_x + 8, y_pos - 12), 12)
            pygame.draw.circle(gameDisplay, LEAF_MID, (tree_x, y_pos - 26), 14)

            # e. Highlight Daun (Terang / Depan)
            pygame.draw.circle(gameDisplay, LEAF_LIGHT, (tree_x - 4, y_pos - 16), 8)
            pygame.draw.circle(gameDisplay, LEAF_LIGHT, (tree_x + 3, y_pos - 28), 8)


# ==========================================
# FUNGSI UTAMA GAME LOOP
# ==========================================
def game_loop():
    # Posisi X awal mobil: di tengah layar
    x = (display_width / 2) - (car_width / 2)
    # Posisi Y awal mobil: di bagian bawah layar
    y = (display_height * 0.65)

    # Variabel untuk menyimpan perubahan posisi X (kecepatan horizontal)
    x_change = 0

    # Variable animasi gerakan jalanan
    track_y = 0

    # --- Parameter Awal Musuh ---
    thing_width = car_width # Lebar musuh (disamakan dengan mobil)
    thing_height = car_height # Tinggi musuh (disamakan dengan mobil)
    thing_startx = random.randrange(ROAD_LEFT, ROAD_RIGHT - thing_width) # Posisi X acak
    thing_starty = -600                              # Mulai dari luar atas layar
    thing_speed = 4                                  # Kecepatan awal
           
    dodged = 0       # Skor
    gameExit = False # Flag untuk mengontrol loop

    # Loop utama game: akan terus berjalan selama gameExit = False
    while not gameExit:

        # Menganalisis semua event (input) yang terjadi
        for event in pygame.event.get():
            # Jika user mengklik tombol Close Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Jika tombol keyboard ditekan
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -8 # Bergerak ke kiri
                if event.key == pygame.K_RIGHT:
                    x_change = 8  # Bergerak ke kanan

            # Jika tombol keyboard dilepas
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0  # Berhenti bergerak

        # Update posisi X mobil
        x += x_change

        # Update pergerakan jalanan
        track_y += thing_speed

        # Panggil fungsi gambar lingkungan baru
        draw_environment(track_y)

        # Menggambar dan menggerakkan Musuh
        things(thing_startx, thing_starty, thing_width, thing_height, RED)
        thing_starty += thing_speed # Musuh bergerak ke bawah

        # Menggambar Mobil Player dan Skor
        car(x, y)
        things_dodged(dodged)

        # Logika Batasan Layar (agar mobil tidak keluar layar, tidak crash)
        if x > ROAD_RIGHT - car_width:
            x = ROAD_RIGHT - car_width
        if x < ROAD_LEFT:
            x = ROAD_LEFT

        # Logika Reset Musuh (ketika musuh sudah melewati layar)
        if thing_starty > display_height:
            thing_starty = 0 - thing_height # Reset posisi Y ke atas
            # Reset posisi X secara acak (memastikan di dalam batas layar)
            thing_startx = random.randrange(ROAD_LEFT, ROAD_RIGHT - thing_width)
            dodged += 1
            thing_speed += 0.5 # Tingkatkan kecepatan

        # --- LOGIKA TABRAKAN (HITBOX ASIMETRIS) ---
        # Definisikan pengurangan (reduction) Hitbox agar ramping
        hitbox_margin_x = -240
        hitbox_margin_y = -50

        # Membuat Hitbox untuk Player: Menggunakan ukuran mobil asli tapi di-inflate agar ramping
        player_rect = pygame.Rect(x, y, car_width, car_height).inflate(hitbox_margin_x, hitbox_margin_y)
        # Membuat Hitbox untuk Musuh
        enemy_rect = pygame.Rect(thing_startx, thing_starty, thing_width, thing_height).inflate(hitbox_margin_x, hitbox_margin_y)

        # Cek Tabrakan: colliderect() akan TRUE jika kedua kotak bersentuhan
        if player_rect.colliderect(enemy_rect):
              crash()

        # ==========================================
        # DEBUG MODE: GAMBAR HITBOX (Sekarang Dihapus/Transparan)
        # ==========================================
        pygame.draw.rect(gameDisplay, (0, 255, 0), player_rect, 2)
        pygame.draw.rect(gameDisplay, (255, 0, 0), enemy_rect, 2)
        # ==========================================

        # Memperbarui seluruh layar untuk menampilkan semua perubahan
        pygame.display.update()
        # Mengatur Frame Rate (FPS) agar game berjalan mulus
        clock.tick(60)

# Memulai game pertama kali
game_loop()
# Perintah keluar dari Pygame dan Python
pygame.quit()
quit()