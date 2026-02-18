import customtkinter as ctk
import pyrebase
import random
import string
from datetime import datetime
from tkinter import messagebox

# --- FIREBASE YAPILANDIRMASI ---
config = {
    "apiKey": "AIzaSyDbwcVL09Fc8bNe6h4Tp0AuA772xeObdWg",
    "authDomain": "lawiaw.firebaseapp.com",
    "databaseURL": "https://lawiaw-default-rtdb.firebaseio.com",
    "projectId": "lawiaw",
    "storageBucket": "lawiaw.firebasestorage.app",
    "messagingSenderId": "1026864162658",
    "appId": "1:1026864162658:web:c200ad9c9bae53fb22ee3b"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

class LawiAdminMaster(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LAWIANDREW - MASTER CONTROL CENTER V5")
        self.geometry("700x950")
        ctk.set_appearance_mode("Dark")

        # --- BAŞLIK ---
        ctk.CTkLabel(self, text="🛡️ LAWIANDREW COMMAND CENTER", font=("Orbitron", 24, "bold"), text_color="#2CC985").pack(pady=20)

        # --- 1. HABER VE DUYURU SİSTEMİ ---
        self.create_section("📢 HABER YAYINLAMA")
        self.news_entry = ctk.CTkEntry(self, width=550, placeholder_text="Ana ekranda kayacak haber metni...")
        self.news_entry.pack(pady=5)
        
        btn_f = ctk.CTkFrame(self, fg_color="transparent")
        btn_f.pack(pady=5)
        ctk.CTkButton(btn_f, text="YAYINLA", width=270, fg_color="#2CC985", text_color="black", font=("Roboto", 13, "bold"), command=self.publish_news).pack(side="left", padx=5)
        ctk.CTkButton(btn_f, text="HABERİ SİL", width=270, fg_color="#e74c3c", command=self.delete_news).pack(side="left", padx=5)

        # --- 2. GÜNCELLEME NOTLARI (CHANGELOG) ---
        self.create_section("📜 GÜNCELLEME NOTLARI EKLE")
        self.log_ver = ctk.CTkEntry(self, width=550, placeholder_text="Versiyon No (Örn: v1.1)")
        self.log_ver.pack(pady=5)
        self.log_text = ctk.CTkTextbox(self, width=550, height=80)
        self.log_text.pack(pady=5)
        ctk.CTkButton(self, text="NOTU SİSTEME EKLE", width=550, command=self.add_changelog).pack(pady=5)

        # --- 3. LİSANS MAKİNESİ (PARA BASMA) ---
        self.create_section("🔑 LİSANS ÜRETİCİ")
        self.cust_name = ctk.CTkEntry(self, width=550, placeholder_text="Müşteri Adı / Not")
        self.cust_name.pack(pady=5)
        
        lic_f = ctk.CTkFrame(self, fg_color="transparent")
        lic_f.pack(pady=5)
        self.time_val = ctk.CTkEntry(lic_f, width=150, placeholder_text="Miktar")
        self.time_val.pack(side="left", padx=5)
        self.time_unit = ctk.CTkOptionMenu(lic_f, values=["Dakika", "Saat", "Gün", "Sonsuz"], width=150)
        self.time_unit.pack(side="left", padx=5)
        self.m_type = ctk.CTkOptionMenu(lic_f, values=["Basic", "Pro", "Premium"], width=150)
        self.m_type.pack(side="left", padx=5)

        ctk.CTkButton(self, text="LİSANS OLUŞTUR VE YÜKLE", width=550, height=45, fg_color="#2CC985", text_color="black", font=("Roboto", 15, "bold"), command=self.generate_lic).pack(pady=10)
        self.res_lic = ctk.CTkEntry(self, width=550, justify="center", font=("Consolas", 18, "bold"), text_color="#2CC985")
        self.res_lic.pack(pady=5)

        # --- 4. SİSTEM VERSİYON KONTROL ---
        self.create_section("🚀 VERSİYON VE İSTATİSTİK")
        ver_f = ctk.CTkFrame(self, fg_color="transparent")
        ver_f.pack(pady=5)
        self.ver_entry = ctk.CTkEntry(ver_f, width=200, placeholder_text="Yeni Versiyon (Örn: 1.1)")
        self.ver_entry.pack(side="left", padx=5)
        ctk.CTkButton(ver_f, text="SÜRÜMÜ KİLİTLE", fg_color="red", command=self.update_version).pack(side="left", padx=5)

        self.stat_label = ctk.CTkLabel(self, text="Aktif Kullanıcı: ...", font=("Roboto", 14, "bold"))
        self.stat_label.pack(pady=10)

        self.refresh_stats()

    def create_section(self, text):
        ctk.CTkLabel(self, text="----------------------------------------------------------------", text_color="#333").pack()
        ctk.CTkLabel(self, text=text, font=("Roboto", 14, "bold"), text_color="#2CC985").pack(pady=5)

    def publish_news(self):
        db.child("news").set(self.news_entry.get())
        messagebox.showinfo("Başarılı", "Haber yayına girdi!")

    def delete_news(self):
        db.child("news").remove()
        messagebox.showinfo("Başarılı", "Haber silindi!")

    def add_changelog(self):
        v = self.log_ver.get()
        t = self.log_text.get("1.0", "end-1c")
        if v and t:
            db.child("changelog").child(v).set(t)
            messagebox.showinfo("Başarılı", "Güncelleme notu eklendi!")
        else: messagebox.showwarning("Uyarı", "Boş bırakma!")

    def generate_lic(self):
        try:
            unit = self.time_unit.get()
            total_sec = 315360000 if unit == "Sonsuz" else int(self.time_val.get()) * {"Dakika":60, "Saat":3600, "Gün":86400}[unit]
            code = "LAWI-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            db.child("valid_keys").child(code).set({"duration_seconds": total_sec, "type": self.m_type.get(), "note": self.cust_name.get()})
            self.res_lic.delete(0, "end"); self.res_lic.insert(0, code)
            messagebox.showinfo("Sistem", "Lisans aktif!")
        except: messagebox.showerror("Hata", "Süreyi sayı gir!")

    def update_version(self):
        db.child("system_config").update({"latest_version": self.ver_entry.get()})
        messagebox.showinfo("Sistem", "Versiyon güncellendi!")

    def refresh_stats(self):
        count = db.child("system_config").child("active_users").get().val() or 0
        self.stat_label.configure(text=f"📊 TOPLAM AKTİF KULLANIM: {count}")
        self.after(5000, self.refresh_stats)

if __name__ == "__main__":
    app = LawiAdminMaster()
    app.mainloop()