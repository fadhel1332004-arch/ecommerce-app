import os
import re
import urllib.request
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory, make_response
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'alaaqil_market_secret_key_yemen_2026'

# Ensure asset directories exist
ASSETS_DIR = os.path.join(app.root_path, 'static', 'assets')
UPLOADS_DIR = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Image map to download defaults if missing
IMAGES_MAP = {
    'alhana.jpg': 'https://images.unsplash.com/photo-1571212515416-fef01fc43637?w=500&q=80',
    'nadia.jpg': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=500&q=80',
    'yamani.jpg': 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=500&q=80',
    'kabous.jpg': 'https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=500&q=80',
    'shamlan.jpg': 'https://images.unsplash.com/photo-1548839140-29a749e1bc4e?w=500&q=80',
    'abowald.jpg': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=500&q=80',
    'ghowaizi.jpg': 'https://images.unsplash.com/photo-1534482421-64566f976cfa?w=500&q=80',
    'hail.jpg': 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=500&q=80',
    'sugar.jpg': 'https://images.unsplash.com/photo-1581441363689-1f3c3c414635?w=500&q=80',
    'flour.jpg': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=500&q=80',
    'oil.jpg': 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=500&q=80',
    'tide.jpg': 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=500&q=80',
}

import threading

def download_images():
    headers = {'User-Agent': 'Mozilla/5.0'}
    for fname, url in IMAGES_MAP.items():
        fpath = os.path.join(ASSETS_DIR, fname)
        if not os.path.exists(fpath):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=4) as response, open(fpath, 'wb') as f:
                    f.write(response.read())
            except Exception:
                pass

threading.Thread(target=download_images, daemon=True).start()


ALL_PRODUCTS = [
    {
        "id": 1,
        "name": "زبادي الهناء كبير 500مل",
        "unit": "حبة",
        "price": 350,
        "old_price": None,
        "badge": "الأكثر طلباً",
        "badge_color": "#ff6f00",
        "cat": "ألبان وأجبان",
        "img": "alhana.jpg",
        "featured": True,
        "discount": False,
        "icon": "fa-bottle-droplet",
        "desc": "زبادي طبيعي طازج وكامل الدسم من شركة الهناء، مثالي لوجبات الإفطار والعشاء."
    },
    {
        "id": 2,
        "name": "زبادي يماني  طازج صغير",
        "unit": "حبة",
        "price": 150,
        "old_price": 200,
        "badge": "الأكثر طلباً",
        "badge_color": "#ff6f00",
        "cat": "ألبان وأجبان",
        "img": "nadia.jpg",
        "featured": True,
        "discount": True,
        "icon": "fa-egg",
        "desc": "زبادي نادية حجم صغير مناسب للاستخدام الفردي وللأطفال، قوام ناعم وطعم متوازن."
    },
    {
        "id": 3,
        "name": "حليب يماني ممتاز 1 لتر",
        "unit": "حبة",
        "price": 1500,
        "old_price": None,
        "badge": "رائج",
        "badge_color": "#e65100",
        "cat": "ألبان وأجبان",
        "img": "yamani.jpg",
        "featured": False,
        "discount": False,
        "icon": "fa-glass-water",
        "desc": "حليب مبستر طويل الأجل معقم، غني بالكالسيوم والفيتامينات لجميع أفراد العائلة."
    },
    {
        "id": 4,
        "name": "شاي الكبوس كرتون أحمر",
        "unit": "باكت 250جم",
        "price": 1150,
        "old_price": 1350,
        "badge": "الأكثر طلباً",
        "badge_color": "#ff6f00",
        "cat": "مشروبات وعصائر",
        "img": "kabous.jpg",
        "featured": True,
        "discount": True,
        "icon": "fa-mug-hot",
        "desc": "شاي أسود يمني فاخر حبوب خشنة نخب أول، نكهة مركزة ولون ذهبي أصيل."
    },
    {
        "id": 5,
        "name": "مياه شملان صحية 0.75لتر",
        "unit": "قارورة",
        "price": 150,
        "old_price": None,
        "badge": "الأكثر طلباً",
        "badge_color": "#ff6f00",
        "cat": "مشروبات وعصائر",
        "img": "shamlan.jpg",
        "featured": True,
        "discount": False,
        "icon": "fa-droplet",
        "desc": "مياه شرب نقية وطبيعية معبأة من وادي شملان بأعلى معايير الجودة والسلامة."
    },
    {
        "id": 6,
        "name": "بسكويت أبو ولد شاهي كلاسيك",
        "unit": "باكت",
        "price": 100,
        "old_price": None,
        "badge": "الأكثر طلباً",
        "badge_color": "#ff6f00",
        "cat": "حلويات وبسكويت",
        "img": "abowald.jpg",
        "featured": True,
        "discount": False,
        "icon": "fa-cookie-bite",
        "desc": "البسكويت الكلاسيكي الأصلي المحبوب، خفيف ومقرمش ومثالي مع كوب الشاي الحليب."
    },
    {
        "id": 7,
        "name": "تونة الغويزي لحم أبيض علبة",
        "unit": "علبة",
        "price": 850,
        "old_price": 1050,
        "badge": "الأكثر طلباً",
        "badge_color": "#ff6f00",
        "cat": "معلبات وأغذية",
        "img": "ghowaizi.jpg",
        "featured": True,
        "discount": True,
        "icon": "fa-box-archive",
        "desc": "لحم تونة أبيض فاخر محفوظ في زيت نباتي نقي، صيد بحر المكلا الشهير بجودته."
    },
    {
        "id": 8,
        "name": "صلصة طماطم هائل أنيس باكت",
        "unit": "باكت",
        "price": 200,
        "old_price": None,
        "badge": "رائج",
        "badge_color": "#e65100",
        "cat": "معلبات وأغذية",
        "img": "hail.jpg",
        "featured": False,
        "discount": False,
        "icon": "fa-jar",
        "desc": "معجون طماطم مركز وطبيعي 100% يمنح الأكلات والطبخات لوناً ونكهة غنية."
    },
    {
        "id": 9,
        "name": "سكر السعيد أبيض ناعم",
        "unit": "1 كجم",
        "price": 1100,
        "old_price": 1300,
        "badge": "الأكثر طلباً",
        "badge_color": "#ff6f00",
        "cat": "تموينات أساسية",
        "img": "sugar.jpg",
        "featured": True,
        "discount": True,
        "icon": "fa-bag-shopping",
        "desc": "سكر أبيض نقي بلوري سريع الذوبان، مناسب للحلويات والمشروبات اليومية."
    },
    {
        "id": 10,
        "name": "دقيق البركة فاخر أبيض",
        "unit": "1 كجم",
        "price": 650,
        "old_price": None,
        "badge": "الأكثر طلباً",
        "badge_color": "#ff6f00",
        "cat": "تموينات أساسية",
        "img": "flour.jpg",
        "featured": False,
        "discount": False,
        "icon": "fa-wheat-awn",
        "desc": "طحين أبيض ممتاز منقى ومناسب لجميع أنواع الخبز والكيك والمعجنات المنزلية."
    },
    {
        "id": 11,
        "name": "زيت شروق نقي دوار الشمس",
        "unit": "1.5 لتر",
        "price": 3800,
        "old_price": 4300,
        "badge": "رائج",
        "badge_color": "#e65100",
        "cat": "تموينات أساسية",
        "img": "oil.jpg",
        "featured": True,
        "discount": True,
        "icon": "fa-bottle-water",
        "desc": "زيت دوار الشمس نقي عالي الجودة خفيف على المعدة ومناسب للقلي والطبخ."
    },
    {
        "id": 12,
        "name": "صابون تايد مركز أصلي",
        "unit": "كيس 1.5كجم",
        "price": 2400,
        "old_price": None,
        "badge": "الأكثر طلباً",
        "badge_color": "#ff6f00",
        "cat": "منظفات وعناية",
        "img": "tide.jpg",
        "featured": False,
        "discount": False,
        "icon": "fa-soap",
        "desc": "مسحوق غسيل ذو فاعلية فائقة في إزالة البقع المستعصية مع رائحة انتعاش تدوم طويلاً."
    }
]

CATEGORIES = ["الكل", "ألبان وأجبان", "تموينات أساسية", "مشروبات وعصائر", "معلبات وأغذية", "حلويات وبسكويت", "منظفات وعناية"]

# In-memory orders store fallback (plus session)
SERVER_ORDERS = []

def is_valid_yemeni_name(name: str):
    cleaned = name.strip()
    if len(cleaned) < 3:
        return False
    return bool(re.match(r"^[\u0621-\u064A\u0660-\u0669a-zA-Z\s]+$", cleaned))

def is_valid_yemeni_phone(phone: str):
    cleaned = phone.strip().replace(" ", "").replace("-", "")
    return bool(re.match(r"^(?:(?:\+|00)967)?(7[01378]\d{7})$", cleaned))

@app.route('/')
def home():
    featured_products = [p for p in ALL_PRODUCTS if p.get('featured')]
    carousel_products = featured_products
    return render_template('index.html', 
                           products=ALL_PRODUCTS, 
                           featured=featured_products, 
                           carousel=carousel_products, 
                           categories=CATEGORIES[1:], 
                           active_page='home')

@app.route('/products')
def products():
    selected_cat = request.args.get('cat', 'الكل')
    if selected_cat != 'الكل':
        filtered = [p for p in ALL_PRODUCTS if p['cat'] == selected_cat]
    else:
        filtered = ALL_PRODUCTS
    return render_template('products.html', 
                           products=filtered, 
                           all_products=ALL_PRODUCTS, 
                           categories=CATEGORIES, 
                           selected_cat=selected_cat, 
                           active_page='products')

@app.route('/offers')
def offers():
    discount_products = [p for p in ALL_PRODUCTS if p.get('discount')]
    return render_template('offers.html', products=discount_products, active_page='offers')

@app.route('/cart')
def cart():
    return render_template('cart.html', active_page='cart')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html', active_page='checkout')

@app.route('/orders')
def orders_view():
    user_orders = session.get('orders', [])
    combined = user_orders + [o for o in SERVER_ORDERS if o not in user_orders]
    return render_template('orders.html', orders=combined, active_page='orders')

@app.route('/favorites')
def favorites():
    return render_template('favorites.html', active_page='favorites')

@app.route('/returns')
def returns():
    return render_template('returns.html', active_page='returns')

# API Endpoints
@app.route('/api/products')
def api_products():
    cat = request.args.get('cat')
    q = request.args.get('q', '').strip().lower()
    
    result = ALL_PRODUCTS
    if cat and cat != 'الكل':
        result = [p for p in result if p['cat'] == cat]
    if q:
        result = [p for p in result if q in p['name'].lower() or q in p['cat'].lower()]
        
    return jsonify({'status': 'success', 'count': len(result), 'products': result})

@app.route('/api/product/<int:pid>')
def api_product(pid):
    product = next((p for p in ALL_PRODUCTS if p['id'] == pid), None)
    if not product:
        return jsonify({'status': 'error', 'message': 'المنتج غير موجود'}), 404
    return jsonify({'status': 'success', 'product': product})

@app.route('/api/checkout', methods=['POST'])
def api_checkout():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()
    payment_code = request.form.get('payment_code', 'cod')
    tx_ref = request.form.get('tx_ref', '').strip()
    items_json = request.form.get('items', '[]')
    total_amount = request.form.get('total', '0')

    # Validations
    if not is_valid_yemeni_name(name):
        return jsonify({'status': 'error', 'message': 'يرجى إدخال اسم عميل صحيح (3 أحرف على الأقل وبدون رموز أو أرقام)!'}), 400

    if not is_valid_yemeni_phone(phone):
        return jsonify({'status': 'error', 'message': 'رقم الهاتف غير صالح! يجب أن يكون رقم جوال يمني مكون من 9 أرقام يبدأ بـ (77 أو 78 أو 73 أو 71 أو 70).'}), 400

    if not address or len(address) < 4:
        return jsonify({'status': 'error', 'message': 'يرجى إدخال عنوان توصيل تفصيلي وواضح!'}), 400

    is_wallet = payment_code in ['onecash', 'jeeb', 'floosak']

    receipt_filename = ''
    if 'receipt' in request.files:
        file = request.files['receipt']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOADS_DIR, filename))
            receipt_filename = filename

    if is_wallet and not receipt_filename and not tx_ref:
        return jsonify({'status': 'error', 'message': 'يرجى رفع صورة إشعار السداد أو كتابة رقم العملية للمتابعة!'}), 400

    pay_labels = {
        'cod': 'الدفع عند الاستلام (نقدًا)',
        'onecash': 'محفظة ون كاش (OneCash)',
        'jeeb': 'محفظة جيب (Jeeb)',
        'floosak': 'محفظة فلوسك (Floosak)',
    }
    pay_name = pay_labels.get(payment_code, 'دفع إلكتروني')
    ref_val = tx_ref if tx_ref else (receipt_filename if receipt_filename else 'الدفع نقدًا عند الاستلام')

    user_orders = session.get('orders', [])
    order_num = f"ORD-{len(user_orders) + len(SERVER_ORDERS) + 1:03d}"

    new_order = {
        'id': order_num,
        'name': name,
        'phone': phone,
        'address': address,
        'payment': pay_name,
        'payment_code': payment_code,
        'tx_ref': ref_val,
        'receipt_file': receipt_filename,
        'total': total_amount,
        'items': items_json
    }

    user_orders.append(new_order)
    session['orders'] = user_orders
    SERVER_ORDERS.append(new_order)

    # Build WhatsApp URL
    receipt_note = f"\n*ملف الإشعار المرفق:* {receipt_filename}" if receipt_filename else ""
    wallet_note = f"\n*المحفظة:* {pay_name}\n*المحول إليه:* فاضل الزيلة (773053886)\n*رقم العملية:* {ref_val}{receipt_note}" if is_wallet else f"\n*طريقة الدفع:* {pay_name}"
    
    wa_msg = f"*فاتورة طلب جديد - العاقل ماركت*\n*رقم الطلب:* {order_num}\n*العميل:* {name}\n*الهاتف:* {phone}\n*العنوان:* {address}{wallet_note}\n\n*المبلغ المطلوب: {total_amount} ر.ي*\n_يرجى تأكيد التجهيز والتوصيل وإرفاق صورة الإشعار._"
    
    import urllib.parse
    wa_encoded = urllib.parse.quote(wa_msg)
    wa_url = f"https://api.whatsapp.com/send?phone=967773053886&text={wa_encoded}"

    return jsonify({
        'status': 'success',
        'order': new_order,
        'wa_url': wa_url
    })

@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'manifest.json', mimetype='application/manifest+json')

@app.route('/sw.js')
def serve_sw():
    response = make_response(send_from_directory(os.path.join(app.root_path, 'static'), 'sw.js', mimetype='application/javascript'))
    response.headers['Service-Worker-Allowed'] = '/'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@app.route('/.well-known/assetlinks.json')
def serve_assetlinks():
    return send_from_directory(os.path.join(app.root_path, 'static', '.well-known'), 'assetlinks.json', mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)

# kkk