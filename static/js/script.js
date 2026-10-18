let isGenerating = false;
let targetNavigationUrl = ""; 

async function resimUret() {
    console.log("1. Fonksiyon başladı!"); 

    const promptText = document.getElementById("promptInput").value;
    const generateBtn = document.getElementById("generateBtn");
    const loadingDiv = document.getElementById("loadingSpinner"); 
    const resultImage = document.getElementById("resultImage");
    const downloadBtn = document.getElementById("downloadBtn");
    const placeholderBox = document.getElementById("placeholderBox");

    if (!promptText) {
        alert("Lütfen bir şeyler yazın!");
        return;
    }

    console.log("2. Değişkenler alındı, ekran hazırlanıyor...");

    // KORUMA AKTİF
    isGenerating = true;

    generateBtn.disabled = true;
    generateBtn.innerText = "Çiziliyor...";
    
    if(placeholderBox) placeholderBox.classList.add("hidden");
    if(loadingDiv) loadingDiv.classList.remove("hidden");
    if(resultImage) resultImage.classList.add("hidden");
    if(downloadBtn) downloadBtn.classList.add("hidden");

    try {
        console.log("3. İstek gönderiliyor: /generate");
        
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: promptText })
        });

        console.log("4. Cevap geldi! Durum:", response.status);

        if (!response.ok) {
            throw new Error(`HTTP hatası! Durum: ${response.status}`);
        }

        const data = await response.json();
        console.log("5. Veri okundu:", data);

        if (data.status === "success") {
            resultImage.src = data.image; 
            
            resultImage.onload = function() {
                loadingDiv.classList.add("hidden");
                resultImage.classList.remove("hidden");
                downloadBtn.classList.remove("hidden");
                console.log("6. Resim yüklendi ve gösterildi.");
            }
            
            downloadBtn.onclick = function() {
                const link = document.createElement('a');
                link.href = resultImage.src;
                link.download = 'ebru-eseri.png';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            };

        } else {
            alert("Hata: " + data.message);
            console.error("Backend Hatası:", data.message);
            loadingDiv.classList.add("hidden");
            if(placeholderBox) placeholderBox.classList.remove("hidden");
        }

    } catch (error) {
        console.error("BÜYÜK HATA:", error);
        alert("Bir bağlantı hatası oluştu: " + error.message);
        loadingDiv.classList.add("hidden");
        if(placeholderBox) placeholderBox.classList.remove("hidden");
    } finally {
        console.log("7. İşlem bitti, buton sıfırlanıyor.");
        generateBtn.disabled = false;
        generateBtn.innerText = "ESERİ OLUŞTUR";
        
        // KORUMA KALKTI
        isGenerating = false;
    }
}


// --- LİNKLERE TIKLAMA KORUMASI (ÖZEL MODAL İÇİN) ---
document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("customWarningModal");
    const stayBtn = document.getElementById("modalStayBtn");
    const leaveBtn = document.getElementById("modalLeaveBtn");
    // Tüm 'a' etiketlerini (linkleri) seç
    const allLinks = document.querySelectorAll("a");

    allLinks.forEach(link => {
        link.addEventListener("click", function(e) {
            // Eğer resim üretiliyorsa VE tıklanan şey gerçekten bir başka sayfaya yönlendiriyorsa
            // (href'i var, # veya javascript: değil)
            const href = this.getAttribute("href");
            
            if (isGenerating && href && !href.startsWith("#") && !href.startsWith("javascript:")) {
                // Tarayıcının gitmesini KESİNLİKLE durdur
                e.preventDefault(); 
                e.stopPropagation();
                
                targetNavigationUrl = href; // Gitmek istediği linki hafızaya al
                
                if (modal) {
                    modal.classList.remove("hidden"); // Özel modalı göster
                }
            }
        });
    });

    // Modaldaki butonların işlevleri
    if (stayBtn && leaveBtn && modal) {
        stayBtn.addEventListener("click", () => {
            modal.classList.add("hidden"); 
            targetNavigationUrl = "";
        });

        leaveBtn.addEventListener("click", () => {
            isGenerating = false; // Korumayı kaldır (artık gidebilir)
            
            // Tarayıcının 'beforeunload' uyarısını ezmek için window olayını temizleyelim
            window.onbeforeunload = null; 

            window.location.href = targetNavigationUrl; // Linke git
        });
    }
});

// --- SEKME KAPATMA / YENİLEME KORUMASI (Tarayıcı Standart Uyarısı) ---
// Bunu sadece kullanıcı F5'e basarsa veya sekmeyi X'ten kapatırsa kullanacağız.
// Nav linklerine basınca bizim Modal çıkacak.
window.onbeforeunload = function(e) {
    if (isGenerating) {
        const msg = "Eseriniz üretiliyor, ayrılmak istiyor musunuz?";
        e.returnValue = msg;
        return msg;
    }
};

// --- NAVBAR SCROLL ANİMASYONU ---
window.addEventListener('scroll', function() {
    const header = document.getElementById('mainHeader');
    if (header) {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }
});

// --- NASIL ÇALIŞIR SAYFASI TİPOGRAFİ ANİMASYONU ---
document.addEventListener('DOMContentLoaded', function() {
    if (!document.querySelector('.timeline-container')) return;

    const observerOptions = { threshold: 0.3 };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const row = entry.target;
                row.classList.add('visible');

                const heading = row.querySelector('.typewriter-heading');
                const para = row.querySelector('.typewriter-text');

                if (!heading.classList.contains('typed')) {
                    typeWriter(heading, heading.getAttribute('data-text'), 50, true); 
                    heading.classList.add('typed');
                    
                    setTimeout(() => {
                        typeWriter(para, para.getAttribute('data-text'), 20, false); 
                    }, 1000);
                }
            }
        });
    }, observerOptions);

    document.querySelectorAll('.step-row').forEach(row => {
        observer.observe(row);
    });
});

function typeWriter(element, text, speed, keepCursor = false) {
    let i = 0;
    element.innerHTML = ""; 
    element.classList.add('typing-cursor'); 

    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        } else {
            if (!keepCursor) {
                element.classList.remove('typing-cursor'); 
            }
        }
    }
    type();
}