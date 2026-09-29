// State Management via localStorage
let cart = JSON.parse(localStorage.getItem('alaaqil_cart')) || {};
let favorites = new Set(JSON.parse(localStorage.getItem('alaaqil_favorites')) || []);

// Helper: Save State
function saveState() {
  localStorage.setItem('alaaqil_cart', JSON.stringify(cart));
  localStorage.setItem('alaaqil_favorites', JSON.stringify(Array.from(favorites)));
  updateCartBadge();
}

// Helper: Toast Notifications
function showToast(message) {
  let toast = document.getElementById('toast-bar');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast-bar';
    toast.className = 'toast-bar';
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => {
    toast.classList.remove('show');
  }, 2000);
}

// Update Cart Badge Counter
function updateCartBadge() {
  const badge = document.getElementById('cart-badge-count');
  if (badge) {
    const totalQty = Object.values(cart).reduce((sum, item) => sum + item.qty, 0);
    badge.textContent = totalQty;
  }
}

// Add Item to Cart
function addToCart(product, qty = 1) {
  const id = product.id;
  if (cart[id]) {
    cart[id].qty += qty;
  } else {
    cart[id] = { product: product, qty: qty };
  }
  saveState();
  showToast(`تمت إضافة (${qty}) من ${product.name} إلى السلة`);
}

// Toggle Favorite State
function toggleFav(product, btnElement) {
  const id = product.id;
  let msg = '';
  if (favorites.has(id)) {
    favorites.delete(id);
    msg = `تم حذف ${product.name} من المفضلة`;
    if (btnElement) {
      btnElement.classList.remove('active');
      btnElement.innerHTML = '<i class="fa-regular fa-heart"></i>';
    }
  } else {
    favorites.add(id);
    msg = `تمت إضافة ${product.name} إلى المفضلة`;
    if (btnElement) {
      btnElement.classList.add('active');
      btnElement.innerHTML = '<i class="fa-solid fa-heart"></i>';
    }
  }
  saveState();
  showToast(msg);
  
  // If on favorites page, re-render
  if (window.location.pathname === '/favorites') {
    location.reload();
  }
}

// Change Quantity in Cart
function changeQty(pid, delta) {
  if (cart[pid]) {
    cart[pid].qty += delta;
    if (cart[pid].qty <= 0) {
      delete cart[pid];
    }
    saveState();
    if (typeof renderCartView === 'function') {
      renderCartView();
    }
  }
}

// Product Details Modal
let modalQty = 1;
let currentModalProduct = null;

function openProductDetails(pid) {
  fetch(`/api/product/${pid}`)
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        const p = data.product;
        currentModalProduct = p;
        modalQty = 1;

        document.getElementById('modal-title').textContent = p.name;
        document.getElementById('modal-price').textContent = `${p.price} ر.ي`;
        document.getElementById('modal-badge').textContent = p.badge;
        document.getElementById('modal-badge').style.backgroundColor = p.badge_color;
        document.getElementById('modal-meta').textContent = `الوحدة: ${p.unit} | القسم: ${p.cat}`;
        document.getElementById('modal-desc').textContent = p.desc || '';
        document.getElementById('modal-qty-val').textContent = '1';

        const imgEl = document.getElementById('modal-img');
        const iconEl = document.getElementById('modal-fallback');
        if (p.img) {
          imgEl.src = `/static/assets/${p.img}`;
          imgEl.style.display = 'block';
          iconEl.style.display = 'none';
        } else {
          imgEl.style.display = 'none';
          iconEl.style.display = 'flex';
        }

        const modal = document.getElementById('product-modal');
        modal.classList.add('active');
      }
    });
}

function closeProductModal() {
  const modal = document.getElementById('product-modal');
  if (modal) modal.classList.remove('active');
}

function incModalQty() {
  modalQty++;
  document.getElementById('modal-qty-val').textContent = modalQty;
}

function decModalQty() {
  if (modalQty > 1) {
    modalQty--;
    document.getElementById('modal-qty-val').textContent = modalQty;
  }
}

function addModalToCart() {
  if (currentModalProduct) {
    addToCart(currentModalProduct, modalQty);
    closeProductModal();
  }
}

// Side Drawer Controls
function openDrawer() {
  const drawer = document.getElementById('drawer-backdrop');
  if (drawer) drawer.classList.add('active');
}

function closeDrawer() {
  const drawer = document.getElementById('drawer-backdrop');
  if (drawer) drawer.classList.remove('active');
}

// Carousel Functionality
function initCarousel() {
  const slides = document.querySelectorAll('.carousel-slide');
  const dots = document.querySelectorAll('.carousel-dots .dot');
  if (!slides.length) return;

  let currentIndex = 0;
  setInterval(() => {
    slides[currentIndex].classList.remove('active');
    if (dots[currentIndex]) dots[currentIndex].classList.remove('active');

    currentIndex = (currentIndex + 1) % slides.length;

    slides[currentIndex].classList.add('active');
    if (dots[currentIndex]) dots[currentIndex].classList.add('active');
  }, 3500);
}

// Search Filter Functionality
function initSearch() {
  const searchInput = document.getElementById('search-input');
  if (!searchInput) return;

  searchInput.addEventListener('input', (e) => {
    const term = e.target.value.trim().lower();
    const cards = document.querySelectorAll('.product-card');
    cards.forEach(card => {
      const name = card.dataset.name ? card.dataset.name.toLowerCase() : '';
      const cat = card.dataset.cat ? card.dataset.cat.toLowerCase() : '';
      if (name.includes(term) || cat.includes(term)) {
        card.style.display = 'flex';
      } else {
        card.style.display = 'none';
      }
    });
  });
}

// Copy Account Number
function copyAccountNumber() {
  navigator.clipboard.writeText('773053886').then(() => {
    showToast('تم نسخ الرقم: 773053886');
  });
}

// PWA Service Worker Registration
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then(reg => {
        console.log('Al-Aaqil Market Service Worker active with scope:', reg.scope);
      })
      .catch(err => {
        console.log('Service Worker registration skipped:', err);
      });
  });
}

// PWA Install Prompt Handler
let deferredInstallPrompt = null;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredInstallPrompt = e;
  
  const isDismissed = localStorage.getItem('alaaqil_install_tip_dismissed');
  const banner = document.getElementById('install-banner');
  if (banner && !isDismissed) {
    banner.style.display = 'flex';
  }
  const tip = document.getElementById('app-install-tip');
  if (tip && !isDismissed) {
    tip.style.display = 'block';
  }
});

// App Installed Event
window.addEventListener('appinstalled', () => {
  showToast('🎉 تم تثبيت تطبيق العاقل ماركت بنجاح على جهازك!');
  deferredInstallPrompt = null;
  const banner = document.getElementById('install-banner');
  if (banner) banner.style.display = 'none';
  const tip = document.getElementById('app-install-tip');
  if (tip) tip.style.display = 'none';
});

// Trigger Native PWA Install or Open Play Store Modal
function triggerPwaInstall() {
  if (deferredInstallPrompt) {
    deferredInstallPrompt.prompt();
    deferredInstallPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        showToast('جاري إضافة تطبيق العاقل ماركت لهاتفك... شكراً لك!');
      } else {
        showToast('تم إلغاء التثبيت. يمكنك دائماً التثبيت لاحقاً (اختياري)');
      }
      deferredInstallPrompt = null;
    });
  } else {
    // If native prompt is not available, open the comprehensive Play Store & Install Guide modal
    openPlayStoreModal();
  }
}

// Open Google Play / App Install Modal
function openPlayStoreModal() {
  const modal = document.getElementById('playstore-modal');
  if (modal) modal.classList.add('active');
}

// Close Google Play Modal
function closePlayStoreModal() {
  const modal = document.getElementById('playstore-modal');
  if (modal) modal.classList.remove('active');
}

// Toggle manual install steps guide
function toggleInstallSteps() {
  const guide = document.getElementById('install-steps-guide');
  if (guide) {
    guide.style.display = (guide.style.display === 'none' || guide.style.display === '') ? 'block' : 'none';
  }
}

// Dismiss Helpful App Tip (Optional step)
function dismissAppTip() {
  const tip = document.getElementById('app-install-tip');
  if (tip) {
    tip.style.transition = 'opacity 0.25s ease, transform 0.25s ease';
    tip.style.opacity = '0';
    tip.style.transform = 'translateY(8px)';
    setTimeout(() => {
      tip.style.display = 'none';
    }, 250);
  }
  localStorage.setItem('alaaqil_install_tip_dismissed', 'true');
  showToast('حسناً! يمكنك دائماً تثبيت التطبيق مستقبلاً من القائمة الجانبية (اختياري)');
}

// Close Install Banner
function closeInstallBanner() {
  const banner = document.getElementById('install-banner');
  if (banner) banner.style.display = 'none';
  localStorage.setItem('alaaqil_install_tip_dismissed', 'true');
}

function installAppPrompt() {
  triggerPwaInstall();
}

// Dynamic Back Button Logic
function handleBackClick() {
  if (document.referrer && document.referrer.includes(window.location.host)) {
    window.history.back();
  } else {
    window.location.href = '/';
  }
}

// Check Tip Dismissed State on Page Load
function checkInstallTipState() {
  const isDismissed = localStorage.getItem('alaaqil_install_tip_dismissed');
  const tip = document.getElementById('app-install-tip');
  const banner = document.getElementById('install-banner');
  
  if (isDismissed === 'true') {
    if (tip) tip.style.display = 'none';
    if (banner) banner.style.display = 'none';
  }
}

// On DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  updateCartBadge();
  initCarousel();
  initSearch();
  checkInstallTipState();
});

