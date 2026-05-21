from flask import Flask, render_template, request
import openrouteservice
import folium
from datetime import datetime

app = Flask(__name__)
client = openrouteservice.Client(key='5b3ce3597851110001cf6248aaa63c5678d84f509bc13522adb804d3')

locations = {
    'Asrama PGSD' : [102.27160069043919, -3.7617418863983096],
    'Danau Unib' : [102.27306446726114, -3.758445851629117],
    'Dekanat FEB' : [102.26862389169713, -3.7617198090691164],
    'Dekanat FISIP' : [102.27417328919393, -3.7590310709254973],
    'Dekanat FKIP' : [102.27504444750583, -3.75753414150989],
    'Dekanat FMIPA' : [102.2747136045303,  -3.756028855847586],
    'Dekanat Hukum' : [102.26844172291675, -3.760583199392584 ],
    'Dekanat Pertanian' : [102.26921964529129, -3.759336210212976 ],
    'Dekanat Teknik' : [102.27670099113969, -3.7584642603667104  ],
    'Fakultas Kedokteran' : [ 102.27803206102215, -3.7551337561874982],
    'GB 1' : [102.27372095056845, -3.7568032921655625],
    'GB 2' : [102.274037554275, -3.7578575751002457 ],
    'GB 3 & 4' : [102.27664495427499, -3.7560850630710587],
    'GB 5' : [102.27650213893024, -3.7553463918453187],
    'GLT' : [102.27191958168342,  -3.75809920273443 ],
    'GSG' : [ 102.27655797563433, -3.757536160753844 ],
    'Gedung C' : [102.26791776641025, -3.7590706965117002],
    'Gedung FKIP' : [102.27746551161644, -3.756364599659421],
    'Gedung Fisika' : [102.27372386940291, -3.7562055013818023],
    'Gedung J' : [102.2697707104651, -3.76030119474263],
    'Gedung K' : [102.26990813916206, -3.761142906184093],
    'Gerbang Keluar Belakang' : [102.27618970824084, -3.7592446156990227],
    'Gerbang Keluar Depan' : [102.26666968496903, -3.758831903679123],
    'Gerbang Masuk Belakang' : [102.27521569504947, -3.759614988399855],
    'Gerbang Masuk Depan' : [102.26779832443637, -3.7597051616151904],
    'Gerbang Masuk Rektorat' : [102.27268704582688, -3.760605072804902],
    'Jurusan Ekonomi Pembangunan' : [102.26894613829127, -3.7617576387695197],
    'Klinik Pratama Unib' : [102.2717675810424, -3.7614596037430554],
    'LAB Agronomi' : [102.27271362771398, -3.7570165757307543 ],
    'LAB Hukum' : [102.26867339480454, -3.7602660084096446 ],
    'LAB Ilmu Tanah' : [102.27012662561205, -3.7592326497010897 ],
    'LAB Teknik' : [102.27690975882886, -3.758891053967651  ],
    'LAB Terpadu Teknik' : [102.27735016612473, -3.7585892834199925],
    'LPTIK' : [102.27501541748192,  -3.7585034389347047],
    'Magister Ilmu Ekonomi' : [102.2686381084575, -3.7624574876125974],
    'Masjid Baitul Hikmah': [102.27600666694858, -3.758945132312725],
    'Masjid Darul Ulum' : [102.2675868394383, -3.757278224804399 ],
    'Mushola Shelter' : [102.27361705847183, -3.7576982064708235],
    'Perpustakaan' : [102.27485462111163, -3.756806076798016],
    'Rektorat': [102.27231460986346, -3.7590495172423495],
    'Ruang Baca Pertanian' : [102.27283662942735, -3.7571162998364276],
    'S2 Matematika' : [102.27543890078353, -3.7580570001381477],
    'Sekretariat BEM FMIPA' : [102.27496036775979,  -3.75578529907203],
    'Sekretariat Teknik' : [102.27733334828312, -3.7581980275566127 ],
    'Sekretariat UKM' : [102.2757012915378, -3.756636058655066],
    'Stadion Unib' : [102.27817155070424, -3.7576442412116946],
    'UPT Bing' : [102.27036307553568, -3.7607740664372096]
}
lokasi_berurutan = sorted(locations.keys())

def buat_polygon_hindar(coord, offset=0.00015):
    lon, lat = coord
    return [[[lon - offset, lat - offset], [lon + offset, lat - offset],
             [lon + offset, lat + offset], [lon - offset, lat + offset],
             [lon - offset, lat - offset]]]

@app.route('/', methods=['GET', 'POST'])
def index():
    peta_html = ''
    pesan_error = ''
    pesan_info = ''
    routes_info = []
    
    if request.method == 'POST':
        lokasi_awal = request.form.get('lokasi_awal')
        lokasi_tujuan = request.form.get('lokasi_tujuan')
        mode_transport = request.form.get('mode_transport', 'driving-car')
        mode_waktu = request.form.get('mode_waktu', 'asli')
        
        # Mapping motor menggunakan profil sepeda agar bisa masuk jalan kampus
        if mode_transport == 'motorcycle':
            profil_ors = 'cycling-regular'
        else:
            profil_ors = mode_transport
            
        if lokasi_awal == lokasi_tujuan:
            pesan_error = 'Lokasi awal dan tujuan tidak boleh sama.'
        else:
            # === LOGIKA DETEKSI WAKTU (ASLI ATAU MANUAL) ===
            if mode_waktu == 'asli':
                now = datetime.now()
                is_weekend = now.weekday() >= 5
                jam_sekarang = now.hour + (now.minute / 60.0)
                teks_waktu = "waktu asli saat ini"
            else:
                sim_hari = request.form.get('sim_hari', 'kerja')
                sim_jam = request.form.get('sim_jam', '12:00')
                
                is_weekend = True if sim_hari == 'libur' else False
                try:
                    h, m = map(int, sim_jam.split(':'))
                    jam_sekarang = h + (m / 60.0)
                except ValueError:
                    jam_sekarang = 12.0 # Fallback jika input jam kosong/error
                    
                teks_waktu = f"simulasi manual ({'Akhir Pekan' if is_weekend else 'Hari Kerja'}, Jam {sim_jam})"

            # === LOGIKA GERBANG ===
            gerbang_tutup = []
            is_jam_operasional = (not is_weekend) and (6.0 <= jam_sekarang < 18.0)
            
            if not is_jam_operasional:
                gerbang_tutup.extend(['Gerbang Masuk Depan', 'Gerbang Keluar Depan', 'Gerbang Keluar Belakang', 'Gerbang Masuk Rektorat'])
                pesan_info = f'Berdasarkan {teks_waktu}, kampus di luar jam operasional. Rute dihitung via Gerbang Masuk Belakang. '
            else:
                pesan_info = f'Berdasarkan {teks_waktu}, semua gerbang beroperasi normal. '
                
            if lokasi_awal in gerbang_tutup or lokasi_tujuan in gerbang_tutup:
                pesan_error = f'Pencarian dibatalkan: Lokasi yang dipilih sedang TUTUP pada {teks_waktu}.'
            else:
                avoid_polygons = [buat_polygon_hindar(locations[g]) for g in gerbang_tutup if g in locations]
                route_coords = [locations[lokasi_awal], locations[lokasi_tujuan]]
                
                req_kwargs = {
                    'coordinates': route_coords,
                    'profile': profil_ors,
                    'format': 'geojson',
                    'alternative_routes': {'share_factor': 0.6, 'target_count': 3}
                }
                
                if avoid_polygons:
                    req_kwargs['options'] = {'avoid_polygons': {'type': 'MultiPolygon', 'coordinates': avoid_polygons}}
                
                try:
                    routes = client.directions(**req_kwargs)
                    jarak_test_km = routes['features'][0]['properties']['summary']['distance'] / 1000
                    
                    if jarak_test_km > 3.0 and profil_ors == 'driving-car':
                        req_kwargs['profile'] = 'foot-walking'
                        routes = client.directions(**req_kwargs)
                        pesan_info += '(Jalur mobil memutar jauh, peta otomatis dialihkan ke jalur setapak).'
                        
                except openrouteservice.exceptions.ApiError:
                    try:
                        req_kwargs['profile'] = 'foot-walking'
                        routes = client.directions(**req_kwargs)
                        pesan_info += '(Jalan kendaraan terisolasi, peta otomatis menampilkan rute pejalan kaki).'
                    except Exception:
                        pesan_error = 'Gagal total. Titik benar-benar tidak dapat dijangkau oleh algoritma.'
                        routes = None

                if not pesan_error and routes:
                    m = folium.Map(location=[-3.758, 102.272], zoom_start=16, tiles='CartoDB positron')
                    
                    for name, coord in locations.items():
                        warna = 'red' if name in gerbang_tutup else ('blue' if name == 'Rektorat' else 'green')
                        icon_type = 'lock' if name in gerbang_tutup else 'building'
                        folium.Marker(location=[coord[1], coord[0]], popup=name, icon=folium.Icon(color=warna, icon=icon_type, prefix='fa')).add_to(m)
                        
                    colors = ['red', 'blue', 'orange']
                    
                    jarak_utama = routes['features'][0]['properties']['summary']['distance'] / 1000
                    jalur_masuk_akal = []
                    
                    for i, feature in enumerate(routes['features']):
                        dist_km = feature['properties']['summary']['distance'] / 1000
                        
                        is_valid = False
                        if i == 0:
                            is_valid = True
                        elif dist_km <= (jarak_utama * 2.5) and dist_km <= 5.0:
                            is_valid = True
                            
                        if is_valid:
                            jalur_masuk_akal.append((i, feature, dist_km))
                            
                    for index_baru, (index_asli, feature, dist_km) in enumerate(jalur_masuk_akal):
                        dur_min = feature['properties']['summary']['duration'] / 60
                        warna_rute = colors[index_baru % len(colors)]
                        
                        routes_info.append({
                            'id': index_baru + 1,
                            'jarak': round(dist_km, 2),
                            'waktu': round(dur_min, 1),
                            'warna': warna_rute,
                            'is_utama': True if index_baru == 0 else False
                        })
                        
                        label = 'Rute Utama' if index_baru == 0 else f'Alternatif {index_baru}'
                        folium.GeoJson(
                            feature, 
                            name=label,
                            tooltip=f'{label}: {dist_km:.2f} km | {dur_min:.1f} menit',
                            style_function=lambda x, col=warna_rute, w=(8 if index_baru==0 else 5), o=(0.9 if index_baru==0 else 0.6): {'color': col, 'weight': w, 'opacity': o}
                        ).add_to(m)
                    
                    peta_html = m.get_root().render()

    return render_template('index.html', 
                           lokasi_list=lokasi_berurutan, 
                           peta_html=peta_html, 
                           pesan_error=pesan_error, 
                           pesan_info=pesan_info,
                           routes_info=routes_info)

if __name__ == '__main__':
    app.run(debug=True)