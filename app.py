from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from deep_translator import GoogleTranslator
import requests
import time

app = Flask(__name__)
CORS(app)  # Tarayıcı güvenlik engellerini aşmak için

# --- AYARLAR ---
# Colab'i açtığında Ngrok linki buraya yapıştırılacak.
# Link "http" ile başlamıyorsa sistem otomatik olarak simülasyon modunda çalışır.
COLAB_API_URL = "https://interoffice-thermostatically-claudia.ngrok-free.dev"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/nasil-calisir")
def nasil_calisir():
    return render_template("nasil_calisir.html")


@app.route("/ornekler")
def ornekler():
    return render_template("ornekler.html")


@app.route("/proje-ekibi")
def proje_ekibi():
    return render_template("proje_ekibi.html")


@app.route("/generate", methods=["POST"])
def generate_image():
    print("\n🔔 --- YENİ İSTEK GELDİ ---")

    try:
        # 1. VERİYİ AL
        data = request.json
        user_prompt_tr = data.get("prompt")
        print(f"📥 Kullanıcı: {user_prompt_tr}")

        if not user_prompt_tr:
            return jsonify({"status": "error", "message": "Boş metin gönderildi!"})

        # 2. ÇEVİRİ YAP (TR -> EN)
        try:
            translator = GoogleTranslator(source="auto", target="en")
            translated_prompt = translator.translate(user_prompt_tr)
            print(f"🔄 Çeviri: {translated_prompt}")
        except Exception as e:
            print(f"⚠️ Çeviri Servisi Hatası: {e}")
            translated_prompt = user_prompt_tr  # Hata olursa Türkçesini kullan

        # 3. PROMPT HAZIRLA (Mühendislik Kısmı)
        # Buradaki ayarlar senin "Altın Ayarların"
        # 3. PROMPT HAZIRLA (Mühendislik Kısmı)
        # Buradaki ayarlar senin "Altın Ayarların"
        
        # 1. Adım: Modelin beynini yıkayacağımız ana stil kelimeleri (EN BAŞTA)
        ebru_stili = "ebru art style, marble texture, liquid art,"
        
        # 2. Adım: LoRA modelini çağıran etiket (EN SONDA)
        lora_etiketi = "<lora:ebru_projesi-01:0.9>"
        
        # 3. Adım: Hepsini Sandviç Yap (Stil + Kullanıcı İsteği + LoRA)
        final_prompt = f"{ebru_stili} {translated_prompt} {lora_etiketi}"
        
        # Modelin kesinlikle YAPMAMASI gereken şeyler (Senin yazdığın harika duruyor)
        negative_prompt = "photorealistic, 3d render, photography, real life, depth of field, background details, ugly, deformed, blurry, text"

        print(f"🚀 Hazırlanan Paket: {final_prompt}")

        # 4. MOD SEÇİMİ (Simülasyon mu, Gerçek mi?)
        if "http" not in COLAB_API_URL:
            # --- SİMÜLASYON MODU ---
            print("⚠️ Colab Linki Yok -> SİMÜLASYON MODU DEVREDE")
            time.sleep(2)  # Gerçekçi olsun diye bekletiyoruz

            return jsonify(
                {
                    "status": "success",
                    "message": "Sistem TEST modunda çalıştı (GPU Bağlı Değil).",
                    "debug_info": f"Çevrilen: {translated_prompt}",
                    # Test resmi (Lale)
                    "image": "https://images.unsplash.com/photo-1572454591674-2739f30d8c40?ixlib=rb-1.2.1&auto=format&fit=crop&w=1024&q=80",
                }
            )

        else:
            # --- GERÇEK GPU BAĞLANTISI ---
            print(f"ep Bağlanılıyor: {COLAB_API_URL}...")

            payload = {
                "prompt": final_prompt,
                "negative_prompt": negative_prompt,
                "steps": 20,  # Hız/Kalite Dengesi
                "cfg_scale": 7,  # Otorite Dengesi
                "width": 1024,
                "height": 1024,
                "sampler_name": "DPM++ 2M",
            }

            # İsteği Colab'e gönder
            response = requests.post(f"{COLAB_API_URL}/sdapi/v1/txt2img", json=payload)

            # Cevabı Kontrol Et
            if response.status_code == 200:
                r_json = response.json()

                # Stable Diffusion resmi "Base64" kodunda gönderir.
                # tarayıcının anlayacağı "data:image" formatına çeviriyoruz.
                image_b64 = r_json["images"][0]
                image_data = f"data:image/png;base64,{image_b64}"

                print("✅ GPU Resmi Başarıyla Üretti!")

                return jsonify(
                    {
                        "status": "success",
                        "message": "Eseriniz GPU tarafından başarıyla üretildi.",
                        "debug_info": f"Çeviri: {translated_prompt}",
                        "image": image_data,
                    }
                )
            else:
                print(f"❌ Colab Hatası: {response.text}")
                return jsonify(
                    {
                        "status": "error",
                        "message": f"GPU Hatası: {response.status_code}",
                    }
                )

    except Exception as e:
        print(f"❌ SUNUCU HATASI: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
