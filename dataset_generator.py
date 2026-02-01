import os
import secrets
import random
from encryption_manager import EncryptionManager 

MASTER_HMAC_KEY = secrets.token_bytes(32)  
TARGET_SIZE_MB = 10                        
TARGET_BYTES = TARGET_SIZE_MB * 1024 * 1024

FILE_SAME_PLAIN = "dataset_same_plaintext.txt"
FILE_SAME_CIPHER = "dataset_same_ciphertext.txt"
FILE_VARIED_PLAIN = "dataset_varied_plaintext.txt"
FILE_VARIED_CIPHER = "dataset_varied_ciphertext.txt"


TURKISH_SENTENCES = [
    
    "Pijamalı hasta yağız şoföre çabucak güvendi.", 
    "Muvaffakiyetsizleştiricileştiriveremeyebileceklerimizdenmişsinizcesine.", 
    "Çekoslavakyalılaştıramadıklarımızdan mısınız?",
    "Şu köşe yaz köşesi, şu köşe kış köşesi, ortada su şişesi.", 
    "Bir berber bir berbere bre berber gel beraber bir berber dükkanı açalım demiş.", 
    "Adaletin kestiği parmak acımaz ama kanar.",
    

    "Kriptografi, verilerin yetkisiz erişime karşı korunmasını sağlayan matematiksel bir disiplindir.",
    "Simetrik şifreleme algoritmalarında gönderici ve alıcı aynı anahtarı kullanır.",
    "Asimetrik şifrelemede ise bir açık anahtar (public key) ve bir gizli anahtar (private key) bulunur.",
    "Hash fonksiyonları, verinin bütünlüğünü doğrulamak için eşsiz özetler oluşturur.",
    "Nesnelerin İnterneti (IoT), fiziksel cihazların birbirleriyle haberleşmesini sağlar.",
    "Büyük veri analitiği, karmaşık veri setlerinden anlamlı desenler çıkarmayı hedefler.",
    "Yapay sinir ağları, insan beyninin çalışma prensibini taklit eden algoritmalardır.",
    "Blok zinciri (Blockchain), merkeziyetsiz ve değiştirilemez bir kayıt defteridir.",
    "Siber güvenlik uzmanları, sistem açıklarını kapatmak için sürekli çalışırlar.",
    "Kuantum bilgisayarlar, klasik bilgisayarların çözemediği problemleri çözme potansiyeline sahiptir.",
    "Bulut bilişim, sunucu maliyetlerini düşürür ve ölçeklenebilirlik sağlar.",
    "Açık kaynak kodlu yazılımlar, topluluk desteğiyle güvenli ve şeffaf bir yapı sunar.",
    "Python, veri bilimi ve yapay zeka alanında en popüler programlama dillerinden biridir.",
    "SQL enjeksiyonu, web uygulamalarında sıkça rastlanan bir güvenlik açığıdır.",
    "İki faktörlü kimlik doğrulama (2FA), hesap güvenliğini önemli ölçüde artırır.",
    "Sıfır gün saldırıları (Zero-day exploits), henüz yaması bulunmayan açıklardan faydalanır.",
    "VPN teknolojisi, internet trafiğini şifreleyerek anonimlik sağlar.",
    "Makine öğrenmesi modelleri, veriden öğrenerek tahmin yapabilen sistemlerdir.",
    "Docker ve Kubernetes, konteyner tabanlı uygulama geliştirmeyi standartlaştırmıştır.",
    "Agile ve Scrum metodolojileri, yazılım geliştirme süreçlerini hızlandırır.",


    "Türkiye, Asya ve Avrupa kıtalarını birbirine bağlayan eşsiz bir konuma sahiptir.",
    "İstanbul Boğazı, tarih boyunca pek çok medeniyetin geçiş güzergahı olmuştur.",
    "Kapadokya'nın peribacaları, volkanik tüflerin erozyona uğramasıyla oluşmuştur.",
    "Pamukkale travertenleri, UNESCO Dünya Mirası Listesi'nde yer almaktadır.",
    "Göbeklitepe, insanlık tarihinin bilinen en eski tapınak kompleksidir.",
    "Karadeniz bölgesi, yeşil doğası ve hırçın deniziyle bilinir.",
    "Akdeniz mutfağı, zeytinyağlı yemekleri ve sağlıklı beslenme alışkanlıklarıyla ünlüdür.",
    "Van Gölü, Türkiye'nin en büyük gölü olup sodalı bir yapıya sahiptir.",
    "Nemrut Dağı, devasa heykelleri ve gün doğumu manzarasıyla büyüleyicidir.",
    "Efes Antik Kenti, Roma döneminden kalma en iyi korunmuş şehirlerden biridir.",

    "Azıcık aşım kaygısız başım, çokça mal göz çıkarmaz.",
    "Damlaya damlaya göl olur, akmasada damlar.",
    "Sakla samanı gelir zamanı, harcama harmanı.",
    "Gülü seven dikenine katlanır, dikeni batan gülünden vazgeçmez.",
    "Ayağını yorganına göre uzat, yoksa üşürsün.",
    "Tatlı dil yılanı deliğinden çıkarır, acı söz dostu düşman eder.",
    "Acele işe şeytan karışır, sabırla pişen koruk helva olur.",
    "Bir elin nesi var, iki elin sesi var.",
    "Üzüm üzüme baka baka kararır, insan insana baka baka alışır.",
    "Keskin sirke küpüne zarar verir, öfke baldan tatlıdır ama sonu acıdır.",
    "Ne ekersen onu biçersin, rüzgar eken fırtına biçer.",

  
    "Hayatta en hakiki mürşit ilimdir, fendir.",
    "Bütün evren, her biri diğerine görünmez iplerle bağlı bir bütündür.",
    "Düşünüyorum, öyleyse varım; var olduğum için sorguluyorum.",
    "Zamanın göreceliği, anın değerini değiştirmese de algısını değiştirir.",
    "Bir kitabın kapağına bakarak içeriğini yargılamak, denizi kıyıdan ibaret sanmaktır.",
    "Sessizlik, bazen en gürültülü çığlıktan daha güçlü bir cevaptır.",
    "Umut, karanlıkta yanan cılız bir mum ışığı gibidir ama asla sönmez.",
    "Özgürlük, başkalarının haklarının başladığı yerde biter.",
    "Gerçek bilgi, neyi bilmediğini bilmektir.",
    "İnsan, doğanın bir parçasıdır ve ona hükmetmek yerine uyum sağlamalıdır.",


    "Mavi gökyüzünde süzülen beyaz bulutlar, pamuk şekerlerini andırıyordu.",
    "Eski radyodan yükselen cızırtılı ses, geçmişe dair anıları canlandırdı.",
    "Kahvenin kokusu, sabahın serinliğine karışarak odaya yayıldı.",
    "Yağmur damlaları cama vururken, dışarıdaki sokak lambası yanıp sönüyordu.",
    "Kütüphanenin tozlu raflarında unutulmuş bir mektup buldu.",
    "Saatin tiktakları, sessiz odada yankılanan tek sesti.",
    "Deniz feneri, fırtınalı gecede gemilere yol gösteriyordu.",
    "Sonbahar rüzgarı, sararmış yaprakları kaldırımlarda savuruyordu.",
    "Çocukların parktaki neşeli çığlıkları, mahalleye hayat veriyordu.",
    "Trenin ritmik sesi, yolcuları derin bir uykuya davet ediyordu.",
    "Kırmızı kaplı defterine, kimseye söyleyemediği sırlarını yazdı.",
    "Eski ahşap evin gıcırdayan merdivenleri, her adımda inliyordu.",
    "Pazar yerindeki renkli tezgahlar, taze meyve ve sebzelerle doluydu.",
    "Gecenin karanlığında parlayan yıldızlar, sonsuzluğu hatırlatıyordu.",
    "Issız bir adada mahsur kalsan yanına alacağın üç şey nedir?",
    "Teknolojinin hızı, insan adaptasyonunun sınırlarını zorluyor.",
    "Dijitalleşme süreci, iş dünyasında köklü değişikliklere neden oldu.",
    "Sürdürülebilirlik, gelecek nesillere yaşanabilir bir dünya bırakmaktır.",
    "İnovasyon, mevcut problemlere yaratıcı ve etkili çözümler bulmaktır.",
    "Girişimcilik, risk almayı ve belirsizlikle başa çıkmayı gerektirir.",
    "Uzaktan çalışma modeli, iş ve özel hayat dengesini yeniden tanımladı.",
    "E-ticaret hacmi, her geçen yıl katlanarak artmaya devam ediyor.",
    "Sosyal medya algoritmaları, kullanıcı davranışlarını analiz ederek içerik sunar.",
    "Kripto paralar, finansal sistemde merkeziyetsiz bir alternatif oluşturdu.",
    "Metaverse kavramı, sanal ve fiziksel gerçekliği birleştirmeyi vadeder."
]


def generate_same_sentence_dataset(cipher_manager):
    print(f"\n--- 1. Senaryo: Aynı Cümle (Repeated) Veri Seti Oluşturuluyor ---")
    
    sentence = "Bu, Türkçenin özel karakterlerini içeren ve frekans analizi direncini test eden sabit bir deneme cümlesidir.\n"
    current_size = 0
    
    with open(FILE_SAME_PLAIN, 'w', encoding='utf-8') as fp, \
         open(FILE_SAME_CIPHER, 'w', encoding='utf-8') as fc:
        
        while current_size < TARGET_BYTES:
            fp.write(sentence)
            
            encrypted_text = cipher_manager.encrypt(sentence)
            
            fc.write(encrypted_text + " /////\n")
            
            current_size += len(sentence.encode('utf-8'))
            
            if current_size % (1024 * 1024) == 0: 
                 print(f"  -> {current_size / (1024*1024):.1f} MB işlendi...")

    print(f"✅ Tamamlandı: {FILE_SAME_PLAIN} ve {FILE_SAME_CIPHER} oluşturuldu.")


def generate_varied_sentence_dataset(cipher_manager):
    print(f"\n--- 2. Senaryo: Farklı Cümleler (Varied) Veri Seti Oluşturuluyor ---")
    
    current_size = 0
    
    with open(FILE_VARIED_PLAIN, 'w', encoding='utf-8') as fp, \
         open(FILE_VARIED_CIPHER, 'w', encoding='utf-8') as fc:
        
        while current_size < TARGET_BYTES:
            sentence = random.choice(TURKISH_SENTENCES) + "\n"
            fp.write(sentence)
            
            encrypted_text = cipher_manager.encrypt(sentence)
            
            fc.write(encrypted_text + " /////\n")
            
            current_size += len(sentence.encode('utf-8'))
            
            if current_size % (2 * 1024 * 1024) < 200: 
                 print(f"  -> {current_size / (1024*1024):.1f} MB işlendi...")

    print(f"✅ Tamamlandı: {FILE_VARIED_PLAIN} ve {FILE_VARIED_CIPHER} oluşturuldu.")


if __name__ == "__main__":
    try:
        manager = EncryptionManager(MASTER_HMAC_KEY)
        print(f"Hedef Boyut: {TARGET_SIZE_MB} MB (Her dosya için)")
        print(f"Cümle Havuzu Boyutu: {len(TURKISH_SENTENCES)} farklı cümle.")
        
        generate_same_sentence_dataset(manager)

        generate_varied_sentence_dataset(manager)
        
        print("\nTüm işlemler başarıyla bitirildi.")
        
    except Exception as e:
        print(f"Bir hata oluştu: {e}")