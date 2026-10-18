import requests
import base64
import os
import time
import csv
import random

# --- AYARLAR ---
API_URL = "http://127.0.0.1:5000/generate"
# KRİTİK DÜZELTME: Eski klasör ve CSV dosyasına geri döndük!
OUTPUT_FOLDER = "ebru_5000_dataset"
CSV_FILE = "ebru_dataset_katalog.csv"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# --- 1. KUSURSUZ VE SABİT CÜMLE LİSTESİ (Yaklaşık 200 Adet) ---
tum_promptlar = [
    # 🌸 1. Geleneksel ve Organik Çiçekler (Sıvı formlara en uygun olanlar)
    "Kırmızı yapraklı ve ince yeşil gövdeli tek bir lale",
    "Su üzerinde süzülen detaylı pembe gül",
    "Birbiri içine geçen renklerle mavi bir sümbül",
    "Sarı ve turuncu damlacıkların oluşturduğu papatya",
    "Kıvrımlı yapraklarıyla mor bir karanfil",
    "Suyun akışına uyum sağlamış beyaz nilüfer",
    "İnce uzun saplı, boynunu bükmüş nergis",
    "Altın sarısı polenleriyle açmış bir ayçiçeği",
    "Dalgalı yeşil zemin üzerinde kırmızı gelincik",
    "Siyah ve kırmızı renklerin karıştığı soyut orkide",
    "Su damlalarından oluşmuş bahar dalları",
    "Pembe kiraz çiçeği yapraklarının su üzerindeki dansı",
    "Koyu mavi arka planda parlayan beyaz zambak",
    "Rüzgarda savruluyormuş gibi duran mor lavanta fırça darbeleri",
    "Turuncu ve kırmızı renkli ateş dikeni çiçeği",
    "Suyun yüzeyine yayılmış dev bir şakayık",
    "Kıvrımlı sarı hatlara sahip hanımeli",
    "Mavi ve beyazın kusursuz uyumuyla mine çiçeği",
    "Girdap şeklini almış yeşil yapraklar arasında kırmızı tomurcuk",
    "Altın rengi damarlara sahip soyut lotus",
    "Turkuaz suda süzülen eflatun çiğdem",
    "İncecik fırça darbeleriyle çizilmiş sarı küpe çiçeği",
    "Gökkuşağı renklerinin birbirine karıştığı fantastik bir çiçek",
    "Gece mavisinin ortasında parlayan gümüş renkli gül",
    "Sıvı damlacıklarının oluşturduğu ortanca kümesi",
    "Kırmızı zemin üzerinde siyah yapraklı anemon",
    "Yeşil ve sarı dalgalar arasında kaybolan yasemin",
    "Keskin olmayan yumuşak hatlı manolya",
    "Suyun merkezinden dışa doğru açılan devasa bir lale",
    "Pastel renklerin hakim olduğu bahar çelengi",

    # 🌀 2. Soyut Akışkan Dinamikler (Battal ve Gelgit Ebru Tarzı)
    "Mavi ve altının kaotik bir şekilde birbirine karıştığı mermer dokusu",
    "Suyun yüzeyinde genişleyen dairesel kırmızı dalgalar",
    "Siyah zemin üzerine sıçramış neon yeşil damlalar",
    "Birbirini kesen paralel renkli çizgiler",
    "Turkuaz ve mor renklerin oluşturduğu sonsuzluk girdabı",
    "Pastel pembe ve mavinin yumuşak geçişleri",
    "Sert fırça darbeleriyle oluşturulmuş zikzak desenler",
    "Bal peteği görünümüne sahip sarı ve kahverengi su yüzeyi",
    "Koyu gri zemin üzerinde patlayan beyaz boya damlaları",
    "Yukarıdan aşağıya süzülen sıvı şelalesi görünümü",
    "Rastgele dağılmış devasa boya halkaları",
    "Rüzgarın suyu dalgalandırması hissini veren yatay çizgiler",
    "Kırmızı ve siyahın agresif bir şekilde çatıştığı doku",
    "Altın yaldızların suyun yüzeyinde oluşturduğu çatlaklar",
    "Renklerin birbirini iterek oluşturduğu hücresel yapılar",
    "Suyun dibine çöküyormuş gibi görünen lacivert gölgeler",
    "Açık yeşil zemin üzerinde yayılan koyu yeşil damarlar",
    "Dört bir yana dağılan simetrik boya patlamaları",
    "İki farklı rengin tam ortada çarpışma anı",
    "Yumuşak geçişli, bulut benzeri soyut formlar",
    "Yılan kavi kıvrımlarla ilerleyen gümüş çizgiler",
    "Koyu morun içinde kaybolan parlak pembe lekeler",
    "Geometrik olmayan tamamen rastgele serpilmiş boyalar",
    "Deniz dalgalarını andıran üst üste binmiş mavi tonlar",
    "Bir ağacın yaş halkalarına benzeyen dairesel formlar",
    "Keskin uçlu yapraklara benzeyen soyut çekmeler",
    "Çölde esen rüzgarın kumda bıraktığı izlere benzeyen sarı dalgalar",
    "Gece gökyüzündeki yıldız tozunu andıran minik damlacıklar",
    "Suyun merkezinde biriken yoğun kırmızı pigment",
    "Çerçeveye doğru dağılarak kaybolan pastel renkler",

    # 🕊️ 3. Hayvan Silüetleri ve Doğal Formlar (Yumuşak Hatlı)
    "Boya dalgalarından oluşmuş zarif bir kuğu silüeti",
    "Mavi suyun içinde süzülen altın renkli koi balığı",
    "Kanatları sıvı gibi birbirine karışan dev bir kelebek",
    "Rüzgarda yelesi dalgalanan şaha kalkmış at silüeti",
    "Siyah ve beyaz dalgaların oluşturduğu zebra deseni",
    "Suyun içinden sıçrayan yunus formu",
    "Renkli damlalardan oluşan uçan bir anka kuşu",
    "Girdap formunda kıvrılmış uyuyan bir kedi silüeti",
    "Suyun yüzeyine yayılmış tavus kuşu tüyleri",
    "Kahverengi ve yeşil tonlarında soyut bir ağaç dalı",
    "Gökyüzünde süzülen kırlangıç sürüsü silüeti",
    "Çölde yürüyen bir devenin soyut ve dalgalı yansıması",
    "Mavi zemin üzerinde süzülen beyaz deniz anası",
    "Renklerin birleşimiyle oluşan baykuş yüzü",
    "Dalgalı yeşil boyalarla oluşturulmuş orman manzarası",
    "Kırmızı ve turuncu renklerin yarattığı alev alan ağaç",
    "Koyu renklerin arasından süzülen gümüş renkli yılan",
    "Kanatları açık bir kartalın gökyüzündeki soyut izi",
    "Suyun içine dağılan mürekkeple oluşmuş ahtapot kollar",
    "Damlaların birleşimiyle ortaya çıkan kaplumbağa kabuğu",
    "Sarı ve siyah renklerin oluşturduğu arı kovanı dokusu",
    "Geyik boynuzlarını andıran kıvrımlı ince çizgiler",
    "Uçuşan sonbahar yapraklarını andıran kızıl damlalar",
    "Suların çekilmesiyle oluşan çorak toprak dokusu",
    "Renkli bulutların içinden geçen uçan ejderha silüeti",
    "Suyun yüzeyinde sıçrayan minik kurbağa formu",
    "Okyanusun derinliklerindeki mercan kayalıklarının soyut hali",
    "Boyaların karışımıyla oluşan kurt kafası silüeti",
    "Gece karanlığında parlayan ateş böceği kümeleri",
    "Suyun akışıyla şekillenmiş devasa bir balina kuyruğu",

    # 🌌 4. Kozmik ve Elementel Temalar
    "Spiral şekilli devasa bir mor galaksi",
    "Güneş patlamalarını andıran sarı ve turuncu dalgalar",
    "Siyah uzay boşluğunda parlayan mavi nebulalar",
    "Dünya'nın uzaydan görünümünü andıran yeşil ve mavi küre",
    "Yıldız kaymasını temsil eden uzun gümüş çizgiler",
    "Bir kara deliğin renkleri yutması gibi içe doğru bükülen formlar",
    "Satürn'ün halkalarını andıran eliptik çizgiler",
    "Ay kraterlerine benzeyen dairesel boya boşlukları",
    "Alev alev yanan kozmik bir ateş topu",
    "Kuzey ışıklarının su üzerindeki akışkan dansı",
    "Kırmızı kum fırtınasını andıran kaotik zemin",
    "Yeraltındaki magmanın kaynamasına benzeyen kırmızı baloncuklar",
    "Buzulların erimesini anımsatan beyaz ve açık mavi geçişler",
    "Koyu siyah bir gecede çakan mor şimşek hatları",
    "Bir gezegenin doğuşunu anımsatan yarım daire formu",
    "Samanyolu galaksisini andıran boya serpiştirmeleri",
    "Derin su altı mağaralarındaki gizemli yeşil ışıklar",
    "Fırtınalı bir denizi andıran koyu lacivert dalgalar",
    "Meteor yağmurunu temsil eden çapraz renk damlaları",
    "Atmosfere giren bir göktaşının bıraktığı soyut duman izi",
    "Suyun elementinin ateş elementiyle savaşını anlatan zıtlık",
    "Toprak elementini temsil eden kahverengi ve yeşil katmanlar",
    "Rüzgarın görünmezliğini hissettiren uçuşan gri tonlar",
    "Gökyüzündeki bulutların gün batımındaki pembe hali",
    "Uzay boşluğunda patlayan bir süpernova",
    "Güneşin kızılcık rengiyle batış anı",
    "Çöken bir yıldızın oluşturduğu yoğun siyah çekirdek",
    "Işığın prizmadan geçerek kırılmasını anımsatan renk tayfı",
    "Dünyanın yörüngesindeki uyduları andıran simetrik noktalar",
    "Bir asteroit kuşağını temsil eden parçalı taş formları",

    # 🎭 5. Duygular ve Konseptler (Metaforik)
    "Hüznü temsil eden iç içe geçmiş gri ve soluk mavi damlalar",
    "Neşeyi ve baharı yansıtan patlayan canlı pastel renkler",
    "Öfkeyi anlatan keskin ve köşeli kırmızı çizgiler",
    "Sakinliği hissettiren yatay ve durgun su yeşili dalgalar",
    "Karmaşayı anlatan, merkeze doğru düğümlenmiş siyah renkler",
    "Umudu simgeleyen, karanlığın içinden çıkan altın bir nokta",
    "Melankoliyi andıran sonbahar tonlarının yavaşça birbirine karışması",
    "Tutkuyu temsil eden derin bordo ve morun ateşli dansı",
    "Özgürlüğü anlatan, çerçevenin dışına taşmaya çalışan mavi fırça darbeleri",
    "Gizemi yansıtan, duman gibi dağılan koyu eflatun lekeler",
    "Zamanın akışını temsil eden birbirine paralel ince çizgiler",
    "Kaosun içindeki düzeni anlatan altın renkli geometrik kırılmalar",
    "Rüya alemini yansıtan sürreal ve bulanık geçişler",
    "Nostaljiyi hissettiren eski sepya fotoğraf tonları",
    "Yalnızlığı temsil eden, boş bir alanda duran tek bir su damlası",
    "Aşkın enerjisini anlatan pembe ve kırmızı kalp benzeri figürler",
    "Korkuyu yansıtan, dibe doğru çekilen karanlık girdaplar",
    ]

# Opsiyonel: Cümlelerin sırasını karıştırmak için
random.shuffle(tum_promptlar)

print(
    f"✅ Toplam {len(tum_promptlar)} adet kusursuz, çeviriye uyumlu Türkçe cümle hazırlandı!"
)

# --- 2. DAHA ÖNCE ÜRETİLENLERİ BUL (Akıllı Hafıza) ---
uretilen_promptlar = set()
en_yuksek_id = 0
csv_yolu = os.path.join(OUTPUT_FOLDER, CSV_FILE)

if os.path.exists(csv_yolu):
    with open(csv_yolu, "r", encoding="utf-8") as f:
        okuyucu = csv.reader(f)
        next(okuyucu, None)
        for satir in okuyucu:
            if len(satir) >= 3:
                uretilen_promptlar.add(satir[2])
                try:
                    mevcut_id = int(satir[0])
                    if mevcut_id > en_yuksek_id:
                        en_yuksek_id = mevcut_id
                except ValueError:
                    pass
    print(f"⚠️ Önceki oturum tespit edildi! Toplam {en_yuksek_id} resim bulundu.")

if en_yuksek_id == 0 and not os.path.exists(csv_yolu):
    with open(csv_yolu, "w", newline="", encoding="utf-8") as f:
        yazici = csv.writer(f)
        yazici.writerow(["ID", "Dosya Adi", "Prompt"])

# --- 3. SERİ ÜRETİM DÖNGÜSÜ ---
print("\n🚀 ÜRETİM BAŞLIYOR... (Sistemi durdurmak için CTRL+C yapabilirsin)")

mevcut_id = en_yuksek_id

with open(csv_yolu, "a", newline="", encoding="utf-8") as f:
    yazici = csv.writer(f)

    for prompt in tum_promptlar:
        if prompt in uretilen_promptlar:
            continue

        mevcut_id += 1

        # Dosya ismi oluştururken karakter düzeltmeleri
        kisaltilmis_isim = (
            "_".join(prompt.split()[:5])
            .replace(",", "")
            .replace(".", "")
            .replace("ı", "i")
            .replace("ş", "s")
            .replace("ğ", "g")
            .replace("ü", "u")
            .replace("ö", "o")
            .replace("ç", "c")
        )
        dosya_adi = f"{mevcut_id:04d}_{kisaltilmis_isim}.png"
        dosya_yolu = os.path.join(OUTPUT_FOLDER, dosya_adi)

        print(f"[{mevcut_id}. Görsel] Çiziliyor: {prompt}")

        try:
            response = requests.post(API_URL, json={"prompt": prompt})

            if response.status_code == 200:
                data = response.json()
                if data["status"] == "success":
                    image_data = data["image"]

                    if "," in image_data:
                        image_data = image_data.split(",")[1]

                    with open(dosya_yolu, "wb") as img_file:
                        img_file.write(base64.b64decode(image_data))

                    yazici.writerow([mevcut_id, dosya_adi, prompt])
                    f.flush()

                    uretilen_promptlar.add(prompt)
                    print(f"   ✔️ Başarılı! -> {dosya_adi}")
                else:
                    print(f"   ❌ Flask Hatası: {data.get('message')}")
            else:
                print(f"   ❌ Bağlantı Hatası: {response.status_code}")

            time.sleep(1.5)

        except KeyboardInterrupt:
            print(
                "\n🛑 İşlem senin tarafından durduruldu! Tam bu noktadan devam edecek."
            )
            break
        except Exception as e:
            print(f"   ⚠️ Beklenmeyen Hata: {e}")
            time.sleep(5)

print("\n🎉 İŞLEM BİTTİ VEYA DURAKLATILDI.")
