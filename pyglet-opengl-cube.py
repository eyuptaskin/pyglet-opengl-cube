import pyglet
import pyglet.gl as gl
from pyglet.window import key

# --- Küp Verilerini Dışarıda Tanımlayalım ---
# Bu, draw_cube fonksiyonunun her seferinde bu listeleri yeniden oluşturmasını engeller.

# 8 köşe noktası (vertex)
VERTICES = [
    (-0.5, -0.5, 0.5),  # 0
    (0.5, -0.5, 0.5),  # 1
    (0.5, 0.5, 0.5),  # 2
    (-0.5, 0.5, 0.5),  # 3
    (-0.5, -0.5, -0.5),  # 4
    (0.5, -0.5, -0.5),  # 5
    (0.5, 0.5, -0.5),  # 6
    (-0.5, 0.5, -0.5)  # 7
]

# 6 yüzey (hangi köşeleri birleştireceği)
FACES = [
    (0, 1, 2, 3),  # Ön
    (1, 5, 6, 2),  # Sağ
    (5, 4, 7, 6),  # Arka
    (4, 0, 3, 7),  # Sol
    (3, 2, 6, 7),  # Üst
    (4, 5, 1, 0)  # Alt
]

# 6 yüzeyin renkleri (R, G, B)
COLORS = [
    (1, 0, 0), (0, 1, 0), (0, 0, 1),
    (1, 1, 0), (1, 0, 1), (0, 1, 1)
]


# --- Ana Pencere Sınıfı ---

class CubeWindow(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 300)

        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)

        # Durum değişkenleri
        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0
        self.rotation_speed = 50.0

        self.translation_x = 0
        self.translation_y = 0
        self.translation_z = -3

        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)

        pyglet.clock.schedule_interval(self.update, 1 / 60.0)

    def draw_cube(self):
        """Önceden tanımlanmış verileri kullanarak küpü çizer."""
        gl.glBegin(gl.GL_QUADS)
        for i, face in enumerate(FACES):
            gl.glColor3f(*COLORS[i])
            for vertex_index in face:
                gl.glVertex3f(*VERTICES[vertex_index])
        gl.glEnd()

    def on_resize(self, width, height):
        """Pencere yeniden boyutlandırıldığında çağrılır (Değişiklik yok)."""
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.gluPerspective(45, width / float(height), 0.1, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        return pyglet.event.EVENT_HANDLED

    def on_draw(self):
        """Ana çizim fonksiyonu (Değişiklik yok)."""
        self.clear()
        gl.glLoadIdentity()

        gl.glTranslatef(self.translation_x, self.translation_y, self.translation_z)
        gl.glRotatef(self.rotation_x, 1, 0, 0)
        gl.glRotatef(self.rotation_y, 0, 1, 0)
        gl.glRotatef(self.rotation_z, 0, 0, 1)

        self.draw_cube()

    def update(self, dt):
        """SADELEŞTİRİLMİŞ update fonksiyonu."""

        # keys[key] basılıysa 1 (True), değilse 0 (False) döner.
        # (self.keys[key.S] - self.keys[key.W]) işlemi:
        # S basılıysa: (1 - 0) = 1
        # W basılıysa: (0 - 1) = -1
        # İkisi de basılı değilse veya ikisi de basılıysa: (0 - 0) = 0 veya (1 - 1) = 0

        # Döndürme
        rot_speed = self.rotation_speed * dt
        self.rotation_x += (self.keys[key.S] - self.keys[key.W]) * rot_speed
        self.rotation_y += (self.keys[key.D] - self.keys[key.A]) * rot_speed
        self.rotation_z += (self.keys[key.E] - self.keys[key.Q]) * rot_speed

        # Öteleme
        move_speed = 1.0 * dt
        self.translation_x += (self.keys[key.RIGHT] - self.keys[key.LEFT]) * move_speed
        self.translation_y += (self.keys[key.UP] - self.keys[key.DOWN]) * move_speed
        self.translation_z += (self.keys[key.PAGEUP] - self.keys[key.PAGEDOWN]) * move_speed

        # Hız Kontrolü (Bu kısım aynı kaldı, çünkü 'or' içeriyor)
        speed_change = 20.0 * dt
        if self.keys[key.NUM_ADD] or self.keys[key.PLUS]:
            self.rotation_speed += speed_change
        if self.keys[key.NUM_SUBTRACT] or self.keys[key.MINUS]:
            self.rotation_speed = max(0, self.rotation_speed - speed_change)


# --- Ana Programı Başlatma ---
if __name__ == '__main__':
    window = CubeWindow(width=800, height=600,
                        caption='OpenGL Küp Animasyonu (Sadeleştirilmiş)',
                        resizable=True)

    print("--- KONTROLLER ---")
    print("Döndürme (Pivot): W, A, S, D, Q, E")
    print("Öteleme (Kaydırma): Yön Tuşları (Oklar)")
    print("Yakınlaş/Uzaklaş (Z-Öteleme): Page Up / Page Down")
    print("Dönüş Hızı: NumPad + / NumPad - (veya +/-)")

    pyglet.app.run()