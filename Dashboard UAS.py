
import streamlit as st
import numpy as np
import pandas as pd
import base64

st.set_page_config(layout="wide", page_title="Uji Statistik", page_icon="📊")

# --- MASUKKAN LINK GAMBAR DI SINI (PASTIKAN LINK RAW) ---
# Contoh link dummy, GANTI DENGAN LINK KAMU SENDIRI
url_bg_utama = "https://raw.githubusercontent.com/yaae72/PEMKOM-D-KELOMPOK-4/refs/heads/main/WhatsApp%20Image%202025-12-07%20at%2003.55.55_d0caecd7.jpg"
url_bg_sidebar = "https://raw.githubusercontent.com/yaae72/PEMKOM-D-KELOMPOK-4/refs/heads/main/WhatsApp%20Image%202025-12-07%20at%2003.52.47_11c07b0e.jpg"
url_flowchart = "https://raw.githubusercontent.com/yaae72/PEMKOM-D-KELOMPOK-4/refs/heads/main/flowchart.jpg"

# --- CSS STYLING ---
st.markdown(f"""
<style>
    /* Background Utama */
    [data-testid="stAppViewContainer"] {{
        background-image: url("{url_bg_utama}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white !important;
    }}
    [data-testid="stAppViewContainer"] h1, 
    [data-testid="stAppViewContainer"] h2, 
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] li, 
    [data-testid="stAppViewContainer"] span {{
        color: white !important; /* Biru tua elegan */
        text-shadow: 
            0 0 6px #0a1a3d,      /* glow halus */
            0 0 10px #0a1a3d,     /* glow medium */
            0 0 14px #0a1a3d;     /* glow elegan */
    }}

    /* Background Sidebar */
    [data-testid="stSidebar"] {{
        background-image: url("{url_bg_sidebar}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: white !important;
    }}
    
    /* Agar tulisan terbaca (opsional: tambah background semi-transparan di teks) */
    [data-testid="stSidebar"] * {{
        color: white !important;
        text-shadow:
            0 0 6px #0a1a3d,
            0 0 10px #0a1a3d,
            0 0 14px #0a1a3d;
    }}
    [data-testid="stSidebar"] * {{ color: white !important; }}
    [data-testid="stSidebar"] h1, h2, h3 {{ color: white !important; }}
</style>
""", unsafe_allow_html=True)

# ==============================================================
# 🌌 CUSTOM SPACE THEME (BLUE GALAXY)
# ==============================================================
# ... (kode CSS tetap sama)

space_css = """
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Orbitron', sans-serif !important;
    background: radial-gradient(circle at top, #001133, #000814, #00010f);
    color: #e0eaff !important;
}

h1, h2, h3, h4 {
    color: #78aaff !important;
    text-shadow: 0 0 8px #4ea0ff;
}

.sidebar .sidebar-content {
    background: #001a33;
    color: white;
}

.css-1d391kg {
    background: #001a33 !important;
}

.stButton>button {
    background-color: #001f4d;
    border: 1px solid #4ea0ff;
    color: #cfe3ff;
    padding: 0.6rem;
    border-radius: 10px;
    transition: 0.3s;
}

.stButton>button:hover {
    background-color: #003f87;
    border-color: #77b5ff;
    transform: scale(1.05);
}

.stTabs [data-baseweb="tab"] {
    background: rgba(0, 34, 68, 0.7);
    border-radius: 10px;
    padding: 10px;
    color: #99c2ff;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background: rgba(0, 60, 120, 0.9);
    color: #ffffff !important;
    border-bottom: 2px solid #4ea0ff;
}

.reportview-container {
    background: #000814;
}

.block-container {
    padding-top: 1rem;
}
</style>
"""

st.markdown(space_css, unsafe_allow_html=True)

# ==============================================================
# SIDEBAR (Galaxy themed)
# ==============================================================
# ... (kode sidebar tetap sama)

st.sidebar.markdown(
    """
    <div style='text-align:center; padding:10px; color:#8db2ff'>
        <h2>📊 Menu Navigasi</h2>
        <p>Uji Statistik Parametrik</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Judul di Sidebar
st.sidebar.title("Menu Navigasi Uji Statistik")
st.sidebar.markdown("---")

if 'p_value_pooled' not in st.session_state:
    st.session_state.p_value_pooled = None
if 't_stat_pooled' not in st.session_state:
    st.session_state.t_stat_pooled = 0
if 't_crit_pooled' not in st.session_state:
    st.session_state.t_crit_pooled = 0
if 'df_pooled' not in st.session_state:
    st.session_state.df_pooled = 0
if 'mean1_pooled' not in st.session_state:
    st.session_state.mean1_pooled = 0
if 'mean2_pooled' not in st.session_state:
    st.session_state.mean2_pooled = 0
if 'sd1_pooled' not in st.session_state:
    st.session_state.sd1_pooled = 0
if 'sd2_pooled' not in st.session_state:
    st.session_state.sd2_pooled = 0
if 'mean_diff_pooled' not in st.session_state:
    st.session_state.mean_diff_pooled = 0
if 'sp_pooled' not in st.session_state:
    st.session_state.sp_pooled = 0
if 'hasil_z_2sampel' not in st.session_state:
    st.session_state.hasil_z_2sampel = 0
if 'df_calc' not in st.session_state:
    st.session_state.df_calc = 0

def hitung_p_value(z_score, arah):
    if arah == 'two-sided':
        return 2 * (1 - norm.cdf(abs(z_score)))
    elif arah == 'smaller':
        return norm.cdf(z_score)
    elif arah == 'larger':
        return 1 - norm.cdf(z_score)
    
def tampilkan_kesimpulan_akhir(p_val, alpha):
    st.markdown("---")
    st.subheader("🏁 Kesimpulan Uji Hipotesis")

    with st.container():
            col1, col2 = st.columns([1,2])
            with col1:
                st.metric("Alpha (Taraf Signifikansi)", f"{alpha}")
            with col2:
                signif = p_val < alpha
                keputusan = "Tolak H0" if signif else "Gagal Tolak H0"

                if signif:
                    st.error(f"Keputusan: {keputusan}")
                else:
                    st.success(f"Keputusan: {keputusan}")

            penjelasan = (
                f"Karena **P-Value ({p_val:.4f}) < Alpha ({alpha})**, maka hipotesis nol **ditolak**."
                if signif else
                f"Karena **P-Value ({p_val:.4f}) ≥ Alpha ({alpha})**, maka **tidak cukup bukti** menolak hipotesis nol."
            )
            st.info(penjelasan)

# Menu Navigasi Utama
menu = st.sidebar.selectbox(
    "Pilih Jenis Uji:",
    (
        "Halaman Utama (Flowchart)",
        "Uji Proporsi (1 & 2 Sampel)",
        "Uji Rata-rata 1 Sampel",
        "Uji Rata-rata 2 Sampel Independen (Uji Z)",
        "Uji Kesamaan Varians (F-test)",
        "Uji Rata-rata 2 Sampel Independen (Pooled t-test)",
        "Uji Rata-rata 2 Sampel Independen (Welch t-test)",
        "Uji Rata-rata 2 Sampel Dependen (Paired t-test)"
    )
)

st.sidebar.markdown("""
    <div style='background:rgba(0,40,80,0.6);
                     padding:15px; 
                     border-radius:12px; 
                     margin-top:10px;
                     border:1px solid #4ea0ff;
                     box-shadow:0 0 8px #4ea0ff;'>
        <h3 style='text-align:center; color:#9ec8ff;'> Anggota Kelompok (I.P.K 4):</h3>
        <p style='text-align:center; color:#cfe3ff;'>
                        <li><strong>Zerlina Aisyah</strong> — 140610250012</li>
                        <li><strong>Tia Lisnawati</strong> — 140610250072</li>
                        <li><strong>Naila Arziki Gunawan — 140610250109</li>
                              <li><strong>Fransiskus Asisi Listyo Nugroho — 140610250085</li>
                                    <li><strong>Ghaisan Adlan Falah — 140610250064</li>
                                          <li><strong>Daffa Azizurrahman — 140610250119</li>
                                                <li><strong>Faris Rasendriya Rasyad — 140s610250087</li>
                                                      <li><strong>Ghaisan Fadillah — 140610250102</li>
            </p>
    </div>
    """,
    unsafe_allow_html=True
)


st.sidebar.info("Aplikasi ini menyediakan penjelasan, rumus, contoh, dan kalkulator interaktif.")

# ==========================================
# 2. HALAMAN BERANDA (FLOWCHART)
# ==========================================
if menu == "Halaman Utama (Flowchart)":
    st.title("Sistem Pemilihan Uji Statistik")
    st.write("Alur Aplikasi ini berdasarkan Flowchart di bawah sehingga gunakan flowchart di bawah ini untuk menentukan uji yang tepat.")

    try:
        st.image(url_flowchart, caption="Flowchart")
    except:
        st.error("Link gambar flowchart juga mungkin salah.")
# 1) Uji Proporsi 1 Sampel
elif "Uji Proporsi" in menu:

        # --- Session State ---
    if 'hasil_1_sampel' not in st.session_state:
        st.session_state['hasil_1_sampel'] = None
    if 'hasil_2_sampel' not in st.session_state:
        st.session_state['hasil_2_sampel'] = None
    
    # --- Fungsi Rumus ---
    def hitung_p_value(z_score, arah):
        if arah == 'two-sided':
            return 2 * (1 - norm.cdf(abs(z_score)))
        elif arah == 'smaller':
            return norm.cdf(z_score)
        elif arah == 'larger':
            return 1 - norm.cdf(z_score)
    
    def tampilkan_kesimpulan_akhir(p_val, alpha):
        st.markdown("---")
        st.subheader("🏁 Kesimpulan Uji Hipotesis")
    
    # Menggunakan container bawaan agar warnanya aman di Dark Mode
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("Alpha (Taraf Signifikansi)", f"{alpha}")
            with col2:
                is_signif = p_val < alpha
                status = "Tolak H0" if is_signif else "Gagal Tolak H0"
                
                # Menggunakan st.error (Merah) atau st.success (Hijau) 
                # Ini otomatis terlihat bagus di Dark/Light mode
                if is_signif:
                    st.error(f"Keputusan: {status}")
                else:
                    st.success(f"Keputusan: {status}")
            
            penjelasan = (
                f"Karena nilai **P-Value ({p_val:.4f}) < Alpha ({alpha})**, maka kita memiliki cukup bukti statistik untuk **Menolak Hipotesis Nol ($H_0$)**."
                if is_signif else
                f"Karena nilai **P-Value ({p_val:.4f}) >= Alpha ({alpha})**, maka kita **Tidak Cukup Bukti** untuk menolak Hipotesis Nol ($H_0$)."
            )
            st.info(penjelasan)

    tipe_uji = st.radio(
    "Pilih tipe uji:",
    ["1 Sampel", "2 Sampel"],
    horizontal=True
    )

    st.title(f" Uji Proporsi - {tipe_uji}")

    # Tabs
    tab_penjelasan, tab_hipotesis, tab_rumus, tab_parameter, tab_contoh, tab_kalkulasi, tab_kriteria_uji, tab_flowchart = st.tabs(
        ["Penjelasan", "Hipotesis", "Rumus", "Parameter", "Contoh", "Kalkulasi", "Kriteria Uji", "Flowchart"]
    )

    # --- TAB 1: PENJELASAN ---
    with tab_penjelasan:
        st.header(f"Konsep Dasar {tipe_uji}")
        if tipe_uji == "1 Sampel":
            st.write("""
            Tujuan:
            Mengukur apakah proporsi populasi sama dengan nilai dugaan tertentu.
            Kapan Digunakan:
            •	Hanya ada 1 sampel.
            •	Ingin menguji proporsi populasi.
            •	Ukuran sampel cukup besar.
            Langkah Perhitungan:
            1.	Tentukan proporsi sampel (jumlah berhasil ÷ total sampel).
            2.	Tetapkan proporsi pembanding dari H0.
            3.	Hitung standar error proporsi.
            4.	Hitung nilai uji (selisih ÷ standar error).
            5.	Tentukan p-value atau nilai kritis.
            6.	Bandingkan nilai uji dengan nilai kritis.
            Keputusan:
            Jika nilai uji lebih ekstrem dari batas → tolak H0.
            """)
          
        else:
            st.write("""
            Tujuan:
            Membandingkan dua proporsi populasi.
            Kapan Digunakan:
            •	Ada dua kelompok independen.
            •	Masing-masing berisi data kategori.
            Langkah Perhitungan:
            1.	Hitung proporsi setiap sampel.
            2.	Gabungkan data untuk menghitung standar error gabungan.
            3.	Hitung selisih proporsi.
            4.	Hitung nilai uji (selisih ÷ standard error).
            5.	Tentukan nilai kritis atau p-value.
            Keputusan:
            Selisih cukup besar → tolak H0.
            """)
            st.markdown("**Hipotesis:**")
            st.latex(r"H_0: p_1 = p_2 \text{ (Proporsi sama)}")
            st.latex(r"H_1: p_1 \neq p_2 \text{ (Berbeda), atau } p_1 > p_2, p_1 < p_2")

    with tab_hipotesis:
        st.header(f"Hipotesis {tipe_uji}")
        if tipe_uji == "1 Sampel":
            st.markdown("**Hipotesis:**")
            st.latex(r"H_0: p = p_0")
            st.latex(r"H_1: p \neq p_0 \text{ (Dua sisi), atau } p < p_0, p > p_0")
        else:
            st.markdown("**Hipotesis:**")
            st.latex(r"H_0: p_1 = p_2 \text{ (Proporsi sama)}")
            st.latex(r"H_1: p_1 \neq p_2 \text{ (Berbeda), atau } p_1 > p_2, p_1 < p_2")

    # --- TAB 3: RUMUS ---
    with tab_rumus:
        st.header(f"Rumus {tipe_uji}")
        
        # Menggunakan st.info agar background menyesuaikan tema (dark/light) otomatis
        if tipe_uji == "1 Sampel":
            st.info("Rumus Z-Test 1 Sampel")
            st.latex(r"Z_{hitung} = \frac{\hat{p} - p_0}{\sqrt{\frac{p_0(1-p_0)}{n}}}")
            st.markdown("""
            **Keterangan Variabel:**
            * $\hat{p} = x/n$ : Proporsi Sampel
            * $p_0$ : Proporsi Hipotesis (Nilai target)
            * $n$ : Jumlah Sampel
            """)
        else:
            st.info("Rumus Z-Test 2 Sampel (Pooled Variance)")
            st.latex(r"Z_{hitung} = \frac{\hat{p}_1 - \hat{p}_2}{\sqrt{\hat{p}_{pool}(1-\hat{p}_{pool}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}")
            st.latex(r"\hat{p}_{pool} = \frac{x_1 + x_2}{n_1 + n_2}")
            st.markdown("""
            **Keterangan Variabel:**
            * $\hat{p}_1, \hat{p}_2$ : Proporsi sampel grup 1 & 2
            * $\hat{p}_{pool}$ : Proporsi gabungan
            * $n_1, n_2$ : Ukuran sampel
            """)

# --- TAB 3: PARAMETER ---
    with tab_parameter:
        st.header(f"Parameter {tipe_uji}")
        if tipe_uji == "1 Sampel":
            st.write("""
            Parameter:
            1. x = jumlah keberhasilan
            2. n = total sampel
            3. p₀ = proporsi dugaan (H0)
            4. α = tingkat signifikansi
            5. alternatif (dua arah, kanan, kiri)
            """)
        else:
            st.write("""
            Parameter:
            1. x₁, n₁ = keberhasilan & total sampel kelompok 1
            2. x₂, n₂ = keberhasilan & total sampel kelompok 2
            3. proporsi gabungan (untuk standard error)
            4. α = tingkat signifikansi
            5.alternatif (dua arah, kanan, kiri)
            """)
            
    # --- TAB 4: CONTOH ---
    with tab_contoh:
        st.header(f"Contoh Perhitungan {tipe_uji}")
        if tipe_uji == "1 Sampel":
            st.write("""
            Misal: n = 100, x = 62, p₀ = 0.60\n
            Tujuan: Mengetahui apakah proporsi populasi = p₀.
            
            1. Hipotesis
            H₀: p = 0.60/n
            H₁: p ≠ 0.60 (dua arah)
            
            2. Langkah Singkat
            - Hitung p̂ = 62/100 = 0.62
            - Hitung Z hitung → ≈ 0.41\n
            Karena dua arah, α = 0.05 → Z kritis = ±1.96
            
            3. Keputusan
            Z hitung = 0.41 tidak masuk daerah kritis.
            ➡ Gagal tolak H₀
            """)
        else:
            st.write("""
            Misal: p̂₁=0.65 (n₁=120), p̂₂=0.50 (n₂=100)

            1.Hipotesis
            H₀: p₁ = p₂
            H₁: p₁ ≠ p₂
            
            2.Langkah Singkat
            Hitung proporsi gabungan p̂c ≈ 0.582
            Hitung Z hitung = 2.24
            α=0.05 dua arah → Z kritis = ±1.96
            
            3.Keputusan
            Z hitung = 2.24 masuk daerah kritis.
            ➡ Tolak H₀
            """)  
            
    # --- TAB 4: KALKULASI ---
    with tab_kalkulasi:
        st.header(f"Kalkulasi Interaktif {tipe_uji}")
        
        col1, col2 = st.columns(2)
        
        # --- INPUT 1 SAMPEL ---
        if tipe_uji == "1 Sampel":
            with col1:
                x = st.number_input("Jumlah Sukses (x)", 0, key="x1")
                n = st.number_input("Total Sampel (n)", 1, value=100, key="n1")
            with col2:
                p0 = st.number_input("Hipotesis Awal ($p_0$)", 0.01, 0.99, 0.5, key="p01")
                alpha = st.selectbox("Taraf Signifikansi ($\\alpha$)", [0.01, 0.05, 0.10], index=1, key="alp1")
                arah = st.selectbox("Arah Hipotesis", ["Two-sided (≠)", "Smaller (<)", "Larger (>)"], key="ar1")

            if st.button("Hitung Statistik Uji", key="btn1"):
                if x > n:
                    st.error("Error: x tidak boleh lebih besar dari n")
                else:
                    phat = x/n
                    se = np.sqrt((p0 * (1 - p0)) / n)
                    z = (phat - p0) / se
                    arah_map = {"Two-sided (≠)": "two-sided", "Smaller (<)": "smaller", "Larger (>)": "larger"}
                    
                    st.session_state['hasil_1_sampel'] = {
                        'z': z, 'phat': phat, 'p0': p0, 
                        'arah': arah_map[arah], 'alpha': alpha
                    }
        
        # --- INPUT 2 SAMPEL ---
        else:
            with col1:
                st.markdown("**Sampel 1**")
                x1 = st.number_input("Sukses 1 ($x_1$)", 0, value=30, key="x21")
                n1 = st.number_input("Total 1 ($n_1$)", 1, value=100, key="n21")
            with col2:
                st.markdown("**Sampel 2**")
                x2 = st.number_input("Sukses 2 ($x_2$)", 0, value=40, key="x22")
                n2 = st.number_input("Total 2 ($n_2$)", 1, value=100, key="n22")
                alpha = st.selectbox("Signifikansi ($\\alpha$)", [0.01, 0.05, 0.10], index=1, key="alp2")
                arah = st.selectbox("Arah Hipotesis", ["Two-sided (≠)", "Smaller (<)", "Larger (>)"], key="ar2")

            if st.button("Hitung Statistik Uji", key="btn2"):
                if x1 > n1 or x2 > n2:
                    st.error("Error: Jumlah sukses melebihi sampel")
                else:
                    p1_hat = x1/n1
                    p2_hat = x2/n2
                    p_pool = (x1 + x2) / (n1 + n2)
                    se = np.sqrt(p_pool * (1 - p_pool) * ((1/n1) + (1/n2)))
                    
                    if se == 0:
                        st.error("Standard Error = 0. Data identik sempurna.")
                    else:
                        z = (p1_hat - p2_hat) / se
                        if "Two-sided" in arah: arah_code = "two-sided"
                        elif "Smaller" in arah: arah_code = "smaller"
                        else: arah_code = "larger"
                        
                        st.session_state['hasil_2_sampel'] = {
                            'z': z, 'p1': p1_hat, 'p2': p2_hat,
                            'arah': arah_code, 'alpha': alpha
                        }

        # --- OUTPUT HASIL ---
        hasil = st.session_state[f'hasil_{"1" if tipe_uji == "1 Sampel" else "2"}_sampel']
        
        if hasil:
            st.markdown("---")
            st.markdown("### 📝 Hasil Statistik")
            
            # Menggunakan st.metric biasa (tanpa box HTML custom) agar aman di dark mode
            c1, c2, c3 = st.columns(3)
            if tipe_uji == "1 Sampel":
                c1.metric("Proporsi Sampel", f"{hasil['phat']:.4f}")
                c2.metric("Proporsi Target", f"{hasil['p0']:.4f}")
            else:
                c1.metric("Proporsi 1", f"{hasil['p1']:.4f}")
                c2.metric("Proporsi 2", f"{hasil['p2']:.4f}")
            
            c3.metric("Z-Score Hitung", f"{hasil['z']:.4f}")
            
            st.write("") # Spasi

        
    with tab_kriteria_uji:
            if st.button("Lihat Keputusan Uji (P-Value)"):
                p_val = hitung_p_value(hasil['z'], hasil['arah'])
                tampilkan_kesimpulan_akhir(p_val, hasil['alpha'])

    with tab_flowchart:
        st.header(f"Flowchart Uji {tipe_uji}")
        if tipe_uji == "1 Sampel":
            st.write("Flowchart referensi untuk Uji Proporsi 1 Sampel")
            url = "https://drive.google.com/file/d/1FU8naWNvFA6eOmRhbUHpZolbFTvAAOIo/preview"
            st.components.v1.iframe(url, width=800, height=1000)
        else:
            st.write("Flowchart referensi untuk Uji Proporsi 2 Sampel")
            url = "https://drive.google.com/file/d/1H_bxtyLgHoLogWZOI0txX78LVAY-sWOB/preview"
            st.components.v1.iframe(url, width=800, height=1000)
             
# 2) Uji Rata-rata 1 Sampel 
elif menu == "Uji Rata-rata 1 Sampel":

    st.header("Uji Rata-rata 1 Sampel (Z-Test & t-Test)")
    tabZ, tabT = st.tabs(["Uji Z (σ diketahui)", "Uji t (σ tidak diketahui)"])

    # =======================  BAGIAN UJI Z  ==========================
    
    with tabZ:
        st.subheader("Uji Z – Rata-rata 1 Sampel (σ diketahui)")
        tab_penjelasan, tab_hipotesis, tab_rumus, tab_parameter, tab_contoh, tab_kalkulasi, tab_kriteria_uji, tab_flowchart= st.tabs(["Konsep", 
                                         "Hipotesis",
                                         "Rumus", "Parameter",
                                         "Contoh Perhitungan Singkat",
                                         "Kalkulasi Interaktif",
                                         "Kriteria Uji", "Flowchart Uji"
                                        ])

        with tab_penjelasan:
            st.header("Penjelasan")
            st.write("""
            Tujuan:
            Menguji apakah rata-rata populasi sama dengan nilai tertentu.\n
            Kapan Digunakan:
            •	Standar deviasi populasi diketahui.
            •	Sampel besar atau populasi berdistribusi normal.
            Langkah Perhitungan:
            1.	Hitung rata-rata sampel.
            2.	Gunakan standar deviasi populasi untuk menghitung standard error.
            3.	Hitung nilai uji (selisih ÷ standard error).
            4.	Cari nilai kritis Z.
            5.	Bandingkan nilai uji dengan nilai kritis.
            Keputusan:
            Nilai uji di luar batas → tolak H0.
            """)
        with tab_hipotesis:
            st.subheader("Hipotesis")
            st.subheader("Two-tail Test")
            st.latex(r"H_0: \mu = \mu_0")
            st.latex(r"H_1: \mu \neq \mu_0")
            
            st.subheader("Lower-tail Test")
            st.latex(r"H_0: \mu \geq \mu_0")
            st.latex(r"H_1: \mu < \mu_0")
            
            st.subheader("Upper-tail Test")
            st.latex(r"H_0: \mu \leq \mu_0")
            st.latex(r"H_1: \mu > \mu_0")
            
        with tab_rumus:
            st.subheader("Rumus")
            st.latex(r"""
            Z = \frac{\bar{x} - \mu_0}{\sigma / \sqrt{n}}
            """)
            st.markdown("""
            *Keterangan:*
            * $\bar{x}$ = Rata-rata sampel
            * $\mu_0$ = Rata-rata populasi (hipotesis)
            * $s$ = Standar deviasi sampel
            * $n$ = Jumlah sampel
            """)

        with tab_parameter:
            st.header("Parameter")
            st.write("""
            Parameter:
            1. x̄ = rata-rata sampel
            2. μ₀ = nilai dugaan dalam H0
            3. σ = standar deviasi populasi (diketahui)
            4. n = ukuran sampel
            5. α = tingkat signifikansi
            6. alternatif (dua arah/kanan/kiri)
            """) 
            
        with tab_contoh:
            st.header("Contoh Perhitungan")
            st.write("""
            Misal: x̄ = 52, μ₀ = 50, σ = 5, n = 36
            
            1.Hipotesis\n
            H₀: μ = 50\n
            H₁: μ ≠ 50
            
            2.Langkah Singkat\n
            Hitung Z hitung = 2.40\n
            Z kritis (α=0.05, dua arah) = ±1.96
            
            3.Keputusan
            2.40 berada di wilayah kritis.
            ➡ Tolak H₀
            """)  
            
        with tab_kalkulasi:
            st.header("Kalkulasi Interaktif (Masukkan Data")
            col1, col2 = st.columns(2)

            with col1:
                xbar_Z = st.number_input("Rata-rata Sampel (x̄)", value=50.0, key="xbar_Z_input")
                sigma_Z = st.number_input("Standar Deviasi Populasi (σ)", min_value=0.0001, value=10.0, key="sigma_Z_input")

            with col2:
                mu0_Z = st.number_input("Nilai Hipotesis (μ₀)", value=55.0, key="mu0_Z_input")
                n_Z = st.number_input("Jumlah Sampel (n)", min_value=1, value=30, key="n_Z_input")

            alpha_Z = st.selectbox("Taraf Signifikansi (α)", [0.01, 0.05, 0.10], index=1, key="alpha_Z_select")
            jenis_uji_Z = st.selectbox("Pilih Jenis Uji:",["Two Tail", "Upper Tail", "Lower Tail"], key="jenis_uji_Z_select")
            
            hitung_Z = st.button("Hitung Uji Z")
            
        with tab_kriteria_uji:
            st.header("Hasil dan Kriteria Uji")
            if hitung_Z:
                Z_val = (xbar_Z - mu0_Z) / (sigma_Z / np.sqrt(n_Z))
            
                if jenis_uji_Z == "Two-tail":
                     p_val_Z = 2 * (1 - stats.norm.cdf(abs(Z_val)))
                elif jenis_uji_Z == "Upper-tail":
                    p_val_Z = 1 - stats.norm.cdf(Z_val)
                else:  # Lower-tail
                    p_val_Z = stats.norm.cdf(Z_val)
            
                colA, colB, colC = st.columns(3)
                
                # Nilai kritis berdasarkan jenis uji
                if jenis_uji_Z == "Two-tail":
                    Z_kritis = stats.norm.ppf(1 - alpha_Z/2)
                elif jenis_uji_Z == "Upper-tail":
                    Z_kritis = stats.norm.ppf(1 - alpha_Z)
                else:  # Lower-tail
                    Z_kritis = stats.norm.ppf(alpha_Z)

                colA.metric("Z-hitung", f"{Z_val:.4f}")
                colB.metric("p-value", f"{p_val_Z:.4f}")
                colC.metric("Z-kritis", f"{Z_kritis:.4f}")
            
                st.markdown("---")
                st.subheader("Kriteria Uji")
            
                # -------------------------
                # Kriteria berdasarkan uji
                # -------------------------
                # Menampilkan kriteria uji berdasarkan jenis_uji_Z (Perbaikan sintaks)
                if jenis_uji_Z == "Two Tail":
                    st.markdown(rf"""
                    *Two-tail Test $H_1: \mu \neq \mu_0$*
                    
                    *Berdasarkan nilai kritis:*
                    * Tolak $H_0$ jika $|Z_{{hitung}}| > Z_{{kritis}} = {Z_kritis:.4f}$  
                    * Gagal tolak $H_0$ jika $|Z_{{hitung}}| \le Z_{{kritis}} = {Z_kritis:.4f}$
                    
                    *Berdasarkan p-value:*
                    * Tolak $H_0$ jika $p\text{{-value}} < \alpha$
                    """)
                elif jenis_uji_Z == "Upper Tail":
                    st.markdown(rf"""
                    *Upper-tail (Right-tail Test) $H_1: \mu > \mu_0$*
                    
                    *Berdasarkan nilai kritis:*
                    * Tolak $H_0$ jika $Z_{{hitung}} > Z_{{kritis}} = {Z_kritis:.4f}$  
                    * Gagal tolak $H_0$ jika $Z_{{hitung}} \le Z_{{kritis}} = {Z_kritis:.4f}$
                    
                    *Berdasarkan p-value:*
                    * Tolak $H_0$ jika $p\text{{-value}} < \alpha$
                    """)
                else:
                    st.markdown(rf"""
                    *Lower-tail (Left-tail Test) $H_1: \mu < \mu_0$*
                    
                    *Berdasarkan nilai kritis:*
                    * Tolak $H_0$ jika $Z_{{hitung}} < Z_{{kritis}} = {Z_kritis:.4f}$  
                    * Gagal tolak $H_0$ jika $Z_{{hitung}} \ge Z_{{kritis}} = {Z_kritis:.4f}$
                    
                    *Berdasarkan p-value:*
                    * Tolak $H_0$ jika $p\text{{-value}} < \alpha$
                    """)
            
                st.markdown("---")
                st.subheader("Keputusan")
            
                # ---------------------------------------
                # KEPUTUSAN AKHIR BERDASARKAN P-VALUE
                # ---------------------------------------
                if p_val_Z < alpha_Z:
                    st.error("*Keputusan: Tolak H0*")
                    
                    if jenis_uji_Z == "Two-tail":
                        st.text("Kesimpulan: Rata-rata berbeda secara signifikan.")
                        st.write(f"|Z-hitung| ({abs(Z_val):.4f}) > Z-kritis ({Z_kritis:.4f})")
                    elif jenis_uji_Z == "Upper-tail":
                        st.text("Kesimpulan: Rata-rata lebih besar secara signifikan.")
                        st.write(f"Z-hitung ({Z_val:.4f}) > Z-kritis ({Z_kritis:.4f})")
                    else:
                        st.text("Kesimpulan: Rata-rata lebih kecil secara signifikan.")
                        st.write(f"Z-hitung ({Z_val:.4f}) < Z-kritis ({Z_kritis:.4f})")
                else:
                    st.success("*Keputusan: Gagal Tolak H0*")
                    st.text("Kesimpulan: Tidak terdapat perbedaan rata-rata yang signifikan.")
                    st.write("Keputusan konsisten dengan kriteria uji.")
            
            else:
                st.info("Masukkan data & klik tombol hitung.")
                
        with tab_flowchart:
            st.header("Flowchart")
            st.write("Flowchart referensi untuk Uji Rata-rata 1 Sampel (Uji z)")
            url = "https://drive.google.com/file/d/1xOO9IhrbANpKBGRKwxUJIhRR8HTqujy2/preview"
            st.components.v1.iframe(url, width=800, height=1000)
        
    # =======================  BAGIAN UJI t  ==========================
   
    with tabT:
        st.subheader("Uji t – Rata-rata 1 Sampel (σ tidak diketahui)")
        tab_penjelasan, tab_hipotesis, tab_rumus, tab_parameter, tab_contoh, tab_kalkulasi, tab_kriteria_uji, tab_flowchart= st.tabs(["Konsep", 
                                         "Hipotesis",
                                         "Rumus", "Parameter",
                                         "Contoh Perhitungan Singkat",
                                         "Kalkulasi Interaktif",
                                         "Kriteria Uji", "Flowchart Uji"
                                        ])

        with tab_penjelasan:
            st.header("Penjelasan")
            st.write("""
            Tujuan:
            Mengetahui apakah rata-rata populasi berbeda dari nilai dugaan ketika standar deviasi populasi tidak diketahui.
            Kapan Digunakan:
            •	Standar deviasi populasi tidak diketahui.
            •	Sampel kecil (n < 30).
            Langkah Perhitungan:
            1.	Hitung rata-rata sampel.
            2.	Hitung standar deviasi sampel.
            3.	Hitung standard error.
            4.	Hitung nilai uji t.
            5.	Gunakan tabel t dengan derajat bebas (n-1).
            Keputusan:
            Jika nilai t lebih ekstrem dari t tabel → tolak H0.
            """)
        with tab_hipotesis:
            st.subheader("Hipotesis Uji")
            st.subheader("Two-tail Test")
            st.latex(r"H_0: \mu = \mu_0")
            st.latex(r"H_1: \mu \neq \mu_0")

            st.subheader("Lower-tail Test")
            st.latex(r"H_0: \mu \geq \mu_0")
            st.latex(r"H_1: \mu < \mu_0")

            st.subheader("Upper-tail Test")
            st.latex(r"H_0: \mu \leq \mu_0")
            st.latex(r"H_1: \mu > \mu_0")

        with tab_rumus:
            st.subheader("Rumus")
            st.latex(r"""
            t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}
            """)

            st.markdown("""
            *Keterangan:*
            - $\bar{x}$ : Rata-rata sampel  
            - $\mu_0$ : Nilai hipotesis  
            - $s$ : Standar deviasi sampel  
            - $n$ : Jumlah sampel  
            - df = n − 1  
            """)

        with tab_parameter:
            st.header("Parameter")
            st.write("""
            Parameter:
            1. x̄ = rata-rata sampel
            2. μ₀ = nilai dugaan
            3. s = standar deviasi sampel
            4. n = ukuran sampel
            5. df = derajat bebas (n−1)
            6. α = tingkat signifikansi
            7. alternatif (dua arah/kanan/kiri)
            """)
        with tab_contoh:
            st.header("Contoh Perhitungan")
            st.code("""
            Misal: x̄ = 5.2, μ₀ = 5, s = 1.1, n = 10
            
            1. Hipotesis
            H₀: μ = 5
            H₁: μ ≠ 5
            
            2. Langkah Singkat
            t hitung ≈ 0.576
            df = 9
            t kritis (df=9, α=0.05 dua arah) = ±2.262
            
            3. Keputusan
            0.576 tidak melewati batas kritis.
            ➡ Gagal tolak H₀
            """)
        with tab_kalkulasi:
            st.header("Kalkulasi Interaktif (Masukkan Data)")
            col1, col2 = st.columns(2)

            with col1:
                xbar_t = st.number_input("Rata-rata Sampel (x̄)", value=48.0)
                s_t = st.number_input("Standar Deviasi Sampel (s)", min_value=0.0001, value=12.0)

            with col2:
                mu0_t = st.number_input("Nilai Hipotesis (μ₀)", value=50.0)
                n_t = st.number_input("Jumlah Sampel (n)", min_value=2, value=25)

            alpha_t = st.selectbox("Taraf Signifikansi", [0.01, 0.05, 0.10], index=1)
            jenis_uji_t = st.selectbox("Pilih Jenis Uji:",["Two Tail", "Upper Tail", "Lower Tail"])

            hitung_t = st.button("Hitung Uji t")
            
        with tab_kriteria_uji:
            st.header("Kriteria dan Hasil Uji")
            if hitung_t:
                
                df = n_t - 1
                t_val = (xbar_t - mu0_t) / (s_t / np.sqrt(n_t))
            
                # P-VALUE
                if jenis_uji_t == "Two-tail":
                    p_val_t = 2 * (1 - stats.t.cdf(abs(t_val), df))
                elif jenis_uji_t == "Upper-tail":
                    p_val_t = 1 - stats.t.cdf(t_val, df)
                else:  # Lower-tail
                    p_val_t = stats.t.cdf(t_val, df)
            
                # NILAI KRITIS
                if jenis_uji_t == "Two-tail":
                    t_kritis = stats.t.ppf(1 - alpha_t/2, df)
                elif jenis_uji_t == "Upper-tail":
                    t_kritis = stats.t.ppf(1 - alpha_t, df)
                else:  # Lower-tail
                    t_kritis = stats.t.ppf(alpha_t, df)

                # OUTPUT NILAI
                colA, colB, colC = st.columns(3)
                colA.metric("t-hitung", f"{t_val:.4f}")
                colB.metric("p-value", f"{p_val_t:.4f}")
                colC.metric("t-kritis", f"{t_kritis:.4f}")
            
                st.markdown("---")
                st.subheader("Kriteria Uji")

                # -------------------------
                # Kriteria Berdasarkan Jenis Uji
                # -------------------------
                # Menampilkan kriteria uji berdasarkan jenis_uji_t (Perbaikan sintaks)
                if jenis_uji_t == "Two Tail":
                    st.markdown(rf"""
                    *Two-tail Test $H_1: \mu \neq \mu_0$*
                    
                    *Berdasarkan nilai kritis:*
                    * Tolak $H_0$ jika $|t_{{hitung}}| > t_{{kritis}} = {t_kritis:.4f}$  
                    * Gagal tolak $H_0$ jika $|t_{{hitung}}| \le t_{{kritis}} = {t_kritis:.4f}$
                    
                    *Berdasarkan p-value:*
                    * Tolak $H_0$ jika $p\text{{-value}} < \alpha$
                    """)
                elif jenis_uji_t == "Upper Tail":
                    st.markdown(rf"""
                    *Upper-tail (Right-tail Test) $H_1: \mu > \mu_0$*
                    
                    *Berdasarkan nilai kritis:*
                    * Tolak $H_0$ jika $t_{{hitung}} > t_{{kritis}} = {t_kritis:.4f}$  
                    * Gagal tolak $H_0$ jika $t_{{hitung}} \le t_{{kritis}} = {t_kritis:.4f}$
                    
                    *Berdasarkan p-value:*
                    * Tolak $H_0$ jika $p\text{{-value}} < \alpha$
                    """)
                else:
                    st.markdown(rf"""
                    *Lower-tail (Left-tail Test) $H_1: \mu < \mu_0$*
                    
                    *Berdasarkan nilai kritis:*
                    * Tolak $H_0$ jika $t_{{hitung}} < t_{{kritis}} = {t_kritis:.4f}$  
                    * Gagal tolak $H_0$ jika $t_{{hitung}} \ge t_{{kritis}} = {t_kritis:.4f}$
                    
                    *Berdasarkan p-value:*
                    * Tolak $H_0$ jika $p\text{{-value}} < \alpha$
                    """)
            
                st.markdown("---")
                st.subheader("Keputusan")
            
                # -------------------------
                # KEPUTUSAN FINAL
                # -------------------------
                if p_val_t < alpha_t:
                    st.error("*Keputusan: Tolak H0*")
            
                    if jenis_uji_t == "Two-tail":
                        st.text("Kesimpulan: Rata-rata berbeda secara signifikan dari μ₀.")
                        st.write(f"|t-hitung| ({abs(t_val):.4f}) > t-kritis ({t_kritis:.4f})")
            
                    elif jenis_uji_t == "Upper-tail":
                        st.text("Kesimpulan: Rata-rata lebih besar secara signifikan.")
                        st.write(f"t-hitung ({t_val:.4f}) > t-kritis ({t_kritis:.4f})")
            
                    else:
                        st.text("Kesimpulan: Rata-rata lebih kecil secara signifikan.")
                        st.write(f"t-hitung ({t_val:.4f}) < t-kritis ({t_kritis:.4f})")
            
                else:
                    st.success("*Keputusan: Gagal Tolak H0*")
                    st.text("Kesimpulan: Tidak terdapat perbedaan rata-rata yang signifikan.")
                    st.write("Keputusan konsisten dengan kriteria uji.")
            
            else:
                st.info("Masukkan data & klik tombol hitung.")
                
        with tab_flowchart:
            st.header("Flowchart")
            st.write("Flowchart referensi untuk Uji Rata-rata 1 Sampel (Uji t)")
        url = "https://drive.google.com/file/d/14BQq-V1QopQrpJMYf5rd3RHb77AhtbvF/preview"
        st.components.v1.iframe(url, width=800, height=1000)
        
# 3) Uji Rata-rata 2 Sampel Independen — Varians Diketahui (Uji Z)
elif menu == "Uji Rata-rata 2 Sampel Independen (Uji Z)":
    st.header("Uji Rata-rata 2 sampel Independen (Z)")
    tab_penjelasan, tab_hipotesis, tab_rumus, tab_parameter, tab_contoh, tab_kalkulasi, tab_kriteria_uji, tab_flowchart= st.tabs(["Konsep", "Hipotesis","Rumus", "Parameter", "Contoh Perhitungan Singkat",
                                     "Statistik Uji","Kriteria Uji", "Flowchart"])
    with tab_penjelasan:
        st.subheader("Penjelasan")
        st.write("""        
        Tujuan:
        Membandingkan rata-rata dua populasi.
        Kapan Digunakan:
        •	Varians populasi kedua kelompok diketahui.
        •	Data berasal dari dua kelompok independen.
        Langkah Perhitungan:
        1.	Hitung rata-rata tiap kelompok.
        2.	Gunakan varians populasi untuk menghitung standard error gabungan.
        3.	Hitung nilai uji Z.
        4.	Cari nilai kritis Z.
        5.	Temukan keputusan dari nilai uji.
        Keputusan:
        Nilai Z lebih ekstrem dari batas → tolak H0.
        """)
    with tab_hipotesis:
        st.header("Hipotesis Statistik")
        st.subheader("Hipotesis Dua Arah (Two-Tailed Test)")
        st.latex(r"H_0: \mu1 = \mu_2")
        st.latex(r"H_1: \mu1 \neq \mu_2")
        st.subheader("Hipotesis Satu Arah (One-Tailed Test)")
        st.subheader("Uji Arah Kanan (Right-Tailed)")
        st.latex(r"H_0: \mu1 <= \mu2")
        st.latex(r"H_1: \mu1 > \mu2")
        st.subheader("Uji Arah Kiri (Left-Tailed)")
        st.latex(r"H_0: \mu1 >= \mu2")
        st.latex(r"H_1: \mu1 < \mu2")
        
    with tab_rumus:
        st.subheader("Rumus")
        st.latex(r"Z = \frac{\bar{x}_1 - \bar{x}_2}{(\sigma_1^2 / n_1)+(\sigma_2^2 / n_2)}")
        st.markdown("""
            **Keterangan:**
            - $xbar_1$ : Rata-rata sampel 1
            - $xbar_2$ : Rata-rata sampel 2
            - $n_1$ : Ukuran Sampel 1
            - $n_2$ : Ukuran Sampel 2
            - $\sigma_1^2$ : Varians Populasi 1
            - $\sigma_2^2$ : Varians Populasi 2
            """)
    with tab_parameter:
        st.header("Parameter")
        st.write("""
        Parameter:
        1. x̄₁, x̄₂ = rata-rata masing-masing sampel
        2. σ₁, σ₂ = standar deviasi populasi (diketahui)
        3. n₁, n₂ = ukuran sampel masing-masing
        4. α dan bentuk H1
        """)
        
    with tab_contoh:
        st.subheader("Contoh Perhitungan")
        st.markdown("""
        Misal:
        x̄₁=100, σ₁=10, n₁=50
        x̄₂=95, σ₂=12, n₂=60
        
        1. Hipotesis\n
        H₀: μ₁ = μ₂\n
        H₁: μ₁ ≠ μ₂
        
        2. Langkah Singkat\n
        Z hitung ≈ 2.38\n
        Z kritis (α=0.05, dua arah) = ±1.96
        
        3. Keputusan
        Z hitung berada pada daerah kritis.
        ➡ Tolak H₀
        """)

    with tab_kalkulasi:
        st.subheader("Kalkulasi Interaktif (Masukkan Data)")

        col1, col2 = st.columns(2)

        with col1:
            xbar1 = st.number_input("Rata-rata Sampel 1 ($\\bar{x}_1$)", value=70.0)
            n1 = st.number_input("Jumlah Sampel 1 ($n_1$)", min_value=1, value=30)
            sigma1 = st.number_input("Standar Deviasi Populasi 1 ($σ_1$)", min_value=0.1, value=10.0)

        with col2:
            xbar2 = st.number_input("Rata-rata Sampel 2 ($\\bar{x}_2$)", value=65.0)
            n2 = st.number_input("Jumlah Sampel 2 ($n_2$)", min_value=1, value=30)
            sigma2 = st.number_input("Standar Deviasi Populasi 2 ($σ_2$)", min_value=0.1, value=10.0)

        alpha = st.selectbox("Signifikansi ($\\alpha$)", [0.01, 0.05, 0.10], index=1)
        arah = st.selectbox("Arah Uji", ["Two-sided (≠)", "Smaller (<)", "Larger (>)"])

        if st.button("Hitung Statistik Uji Z"):
            se = np.sqrt((sigma1**2)/n1 + (sigma2**2)/n2)
            z = (xbar1 - xbar2) / se  

            arah_map = {
                "Two-sided (≠)": "two-sided",
                "Smaller (<)": "smaller",
                "Larger (>)": "larger"
            }

            st.session_state['hasil_z_2sampel'] = {
                'z': z,
                'alpha': alpha,
                'arah': arah_map[arah],
                'xbar1': xbar1,
                'xbar2': xbar2
            }

    with tab_kriteria_uji:
        st.header("Kriteria dan Hasil Uji")
        hasil = st.session_state['hasil_z_2sampel']
        if hasil:
            st.markdown("---")
            st.markdown("### 📝 Hasil Perhitungan")
            a, b, c = st.columns(3)
            a.metric("Rata-rata 1", f"{hasil['xbar1']:.3f}")
            b.metric("Rata-rata 2", f"{hasil['xbar2']:.3f}")
            c.metric("Z Hitung", f"{hasil['z']:.4f}")

            if st.button("Lihat Keputusan Uji (P-Value)"):
                pv = hitung_p_value(hasil['z'], hasil['arah'])
                tampilkan_kesimpulan_akhir(pv, hasil['alpha'])

    with tab_kriteria_uji:
        st.header("Flowchart")
        st.write("Flowchart referensi untuk Uji Rata-rata 2 Sampel Independen (Uji z)")
        url = "https://drive.google.com/file/d/1lXvZnGPtmyQH1N6guD4FF-Oh4BfDnnxH/preview"
        st.components.v1.iframe(url, width=800, height=1000)

# 4) Uji Kesamaan Varians (F-test)
elif menu == "Uji Kesamaan Varians (F-test)" : 
    from scipy.stats import f
    st.header("Uji Kesamaan Varians (F-test)")

    tab_penjelasan, tab_hipotesis, tab_rumus, tab_parameter, tab_contoh, tab_kalkulasi, tab_kriteria_uji, tab_flowchart = st.tabs(["Konsep", "Hipotesis", "Rumus", "Parameter", "Contoh Perhitungan Singkat", "Kalkulasi", "Kriteria Uji", "Flowchart"])
    
    with tab_penjelasan:
        st.subheader("Penjelasan")
        st.write("""
        Tujuan:
        Mengukur apakah varians kedua populasi sama.
        Kapan Digunakan:
        •	Sebelum pooled t-test
        •	Dua sampel independen
        •	Data numerik
        Langkah Perhitungan:
        1.	Hitung varians masing-masing sampel.
        2.	Bentuk rasio varians (varians lebih besar ÷ varians lebih kecil).
        3.	Tentukan derajat bebas masing-masing sampel.
        4.	Bandingkan rasio dengan nilai kritis F.
        Keputusan:
        Jika rasio terlalu besar/kecil → tolak H0.
        """)
    
    with tab_hipotesis:
        st.header("Hipotesis")
        st.subheader("Two-tail Test")
        st.latex(r"H_0: \sigma_1^2 = \sigma_2^2 \quad")
        st.latex(r"H_1: \sigma_1^2 \neq \sigma_2^2 \quad")
        st.subheader("Lower-tail Test")
        st.latex(r"H_0: \sigma_1^2 \geq \sigma_2^2 \quad")
        st.latex(r"H_1: \sigma_1^2 < \sigma_2^2 \quad")
        st.subheader("Upper-tail Test")
        st.latex(r"H_0: \sigma_1^2 \leq \sigma_2^2 \quad")
        st.latex(r"H_1: \sigma_1^2 > \sigma_2^2 \quad")
    
    with tab_rumus:
        st.header("Rumus")
        st.subheader("1. Statistik Uji F:")
        st.latex(r"F = \frac{S_1^2}{S_2^2}")
        st.markdown("""
        **Keterangan:**
        * $S_1^2$ = Varians sampel 1
        * $S_2^2$ = Varians sampel 2
        """)
        st.subheader("2. Derajat bebas:")
        st.latex(r"v_1 = n_1 - 1")
        st.latex(r"v_2 = n_2 - 1")
        st.markdown("""
        **Keterangan:**
        * $v_1$ = Derajat bebas 1
        * $v_2$ = Derajat bebas 2
        * $n_1$ = Jumlah sampel 1
        * $n_2$ = Jumlah sampel 2
        """)
    with tab_parameter:
        st.write("""
        Parameter:
        1. s₁² = varians sampel 1
        2. s₂² = varians sampel 2
        3. n₁, n₂ = ukuran sampel
        4. df₁ = n₁ − 1
        5. df₂ = n₂ − 1
        6. α dan bentuk uji (dua arah/kanan/kiri)
        """)

    with tab_contoh:
        st.header("Contoh Perhitungan")
        st.write("""
        Misal: s₁² = 2, s₂² = 1, n₁=10, n₂=12
        
        1. Hipotesis
        H₀: σ₁² = σ₂²\n
        H₁: σ₁² ≠ σ₂²
        
        2. Langkah Singkat
        F hitung = 2.00\n
        df₁ = 9, df₂ = 11\n
        F kritis dua arah (α=0.05) → lihat tabel F\n
        F(0.025; 9,11) ≈ 0.28\n
        F(0.975; 9,11) ≈ 3.29
        
        3. Keputusan
        2.00 di antara 0.28 dan 3.29 → tidak masuk daerah kritis.
        ➡ Gagal tolak H₀ (varians sama)
        """)
            
    with tab_kalkulasi:
        st.header("Kalkulasi Interaktif (Masukkan Data)")
        
        st.write("Masukkan data X1 dan X2 (dipisahkan koma).")
        
        x1_input = st.text_area("Data X1 (misal: 10,12,9,15,11)")
        x2_input = st.text_area("Data X2 (misal: 8,11,7,14,10)")
        alpha = st.number_input("Masukkan nilai alpha (α):", 0.01, 0.10, 0.05)
        jenis_uji = st.selectbox("Pilih Jenis Uji:",["Two Tail", "Upper Tail", "Lower Tail"])
    
        if st.button("Hitung Uji F"):
            try:
                x1 = np.array(list(map(float, x1_input.split(","))))
                x2 = np.array(list(map(float, x2_input.split(","))))
                
                if len(x1) < 2 or len(x2) < 2:
                    st.error("Jumlah data minimal masing-masing 2!")
                else:
                    s1 = np.var(x1, ddof=1)
                    s2 = np.var(x2, ddof=1)
                    
                    Fh = s1 / s2
                    v1 = len(x2) - 1
                    v2 = len(x1) - 1
    
                    st.session_state["Jenis_uji"] = jenis_uji
                    st.session_state["Fh"] = Fh
                    st.session_state["v1"] = v1
                    st.session_state["v2"] = v2
                    st.session_state["alpha"] = alpha
                    
                    st.subheader("Hasil Perhitungan")
                    st.write(f"F-hitung: {Fh:.2f}")
                    st.write(f"Derajat Bebas 1: {v1}")
                    st.write(f"Derajat Bebas 2: {v2}")

                    st.info("Hasil selengkapnya ada di tab Kriteria Uji")
                    
            except:
                st.error("Format data tidak valid! Pastikan hanya angka dan koma.")
    
    with tab_kriteria_uji:
        st.header("Kriteria dan Hasil Uji")
        if "Fh" in st.session_state:
            Jenis_uji = st.session_state["Jenis_uji"]
            Fh = st.session_state["Fh"]
            v1 = st.session_state["v1"]
            v2 = st.session_state["v2"]
            alpha = st.session_state["alpha"]
    
            Fk = 0.0
            
            if Jenis_uji == "Upper Tail":
                p_value = 1 - f.cdf(Fh, v1, v2)
                Fk_upper = f.ppf(1 - alpha, v1, v2)
                krit = Fh > Fk_upper
                Fk = Fk_upper
                krit_latex = f"F_{{hitung}} > F_{{1-\\alpha, v_1, v_2}} \\quad atau \\quad p\\text{{-value}} < \\alpha"
    
            elif Jenis_uji == "Lower Tail":
                p_value = f.cdf(Fh, v1, v2)
                Fk_lower = f.ppf(alpha, v1, v2)
                krit = Fh < Fk_lower
                Fk = Fk_lower
                krit_latex = f"F_{{hitung}} < F_{{\\alpha, v_1, v_2}} \\quad atau \\quad p\\text{{-value}} < \\alpha"
            else:  # TWO TAIL
                p_value = 2 * min(f.cdf(Fh, v1, v2), 1 - f.cdf(Fh, v1, v2))
    
                Fk_upper = f.ppf(1 - alpha / 2, v1, v2)
                Fk_lower = f.ppf(alpha / 2, v1, v2)
    
                krit = Fh < Fk_lower or Fh > Fk_upper
                krit_latex = f"F_{{hitung}} < F_{{\\alpha/2, v_1, v_2}} \\quad atau \\quad F_{{hitung}} > F_{{1-\\alpha/2, v_1, v_2}} \\quad atau \\quad p\\text{{-value}} < \\alpha"
    
            st.write("### Hasil Perhitungan")
            
            if Jenis_uji == "Two Tail":
                colA, colB, colC, colD, colE = st.columns(5)
                colA.metric("Jenis Uji", Jenis_uji)
                colB.metric("F-hitung", f"{Fh:.2f}")
                colC.metric("F Upper", f"{Fk_upper:.2f}")
                colD.metric("F Lower", f"{Fk_lower:.2f}")
                colE.metric("p-value", f"{p_value:.2f}")
                st.metric("Alpha", f"{alpha:.2f}") # Alpha ditampilkan terpisah
                
            else: # One Tail Tests
                colA, colB, colC, colD, colE = st.columns(5)
                colA.metric("Jenis Uji", Jenis_uji)
                colB.metric("F-hitung", f"{Fh:.2f}")
                colC.metric("F-kritis", f"{Fk:.2f}")
                colD.metric("p-value", f"{p_value:.2f}")
                colE.metric("Alpha", f"{alpha:.2f}")
    
            st.write("### Kriteria Uji")
            st.write("Tolak H₀ jika:")
            st.latex(krit_latex)
    
            if krit or p_value < alpha:
                keputusan = "Tolak H₀"
                st.error(f"Keputusan: {keputusan}")
                
                if jenis_uji == "Two Tail":
                    write = "terdapat perbedaan varians yang signifikan antara dua sampel."
                elif jenis_uji == "Upper Tail":
                    write = "varians sampel pertama secara signifikan lebih besar daripada varians sampel kedua."
                elif jenis_uji == "Lower Tail":
                    write = "varians sampel pertama secara signifikan lebih kecil daripada varians sampel kedua."
    
            else:
                keputusan = "Gagal Tolak H₀"
                st.success(f"Keputusan: {keputusan}")
                
                if jenis_uji == "Two Tail":
                    write = "tidak terdapat perbedaan varians yang signifikan antara dua sampel."
                elif jenis_uji == "Upper Tail":
                    write = "tidak terdapat bukti bahwa varians sampel pertama lebih besar dari varians sampel kedua."
                elif jenis_uji == "Lower Tail":
                    write = "tidak terdapat bukti bahwa varians sampel pertama lebih kecil dari varians sampel kedua."
    
    
            st.write("### Kesimpulan")
            st.info(
                f"Pada taraf signifikansi α = {alpha}, diperoleh keputusan *{keputusan}*, "
                f"dengan demikian {write}"
            )
    
        else:
            st.warning("Silakan lakukan perhitungan terlebih dahulu di Tab Statistik Uji.")

    with tab_flowchart:
        st.header("Flowchart")
        st.write("Flowchart referensi untuk Uji Kesamaan Varians")
        url = "https://drive.google.com/file/d/1IcigHNn55mgUNL7yrQqRWqEq2Kw2ZFlg/preview"
        st.components.v1.iframe(url, width=800, height=1000)

# 5) Pooled t-test (equal variances)
elif menu == "Uji Rata-rata 2 Sampel Independen (Pooled t-test)":
    st.title("Uji Rata-rata Dua Sampel Independen (Pooled t-test)")
    st.write("Digunakan ketika dua sampel independen dibandingkan dengan asumsi varians populasi sama.")

    tab_penjelasan, tab_hipotesis, tab_rumus, tab_parameter, tab_contoh, tab_kalkulasi, tab_kriteria_uji, tab_flowchart = st.tabs([
        "Konsep",
        "Hipotesis",
        "Rumus", "Parameter",
        "Contoh Perhitungan Singkat",
        "Kalkulasi",
        "Kriteria Uji", "Flowchart"
    ])

    with tab_penjelasan:
        st.header("Penjelasan")
        st.write("""
        Tujuan:
        Membandingkan rata-rata dua populasi ketika varians dianggap sama.
        Kapan Digunakan:
        •	Hasil F-test menunjukkan varians sama.
        •	Dua sampel independen.
        Langkah Perhitungan:
        1.	Hitung varians dan rata-rata tiap sampel.
        2.	Gabungkan varians menggunakan metode pooled.
        3.	Hitung standard error gabungan.
        4.	Hitung nilai uji t.
        5.	Gunakan derajat bebas (n1 + n2 − 2).
        Keputusan:
        Nilai t di luar batas → tolak H0.
        """)
    
    with tab_hipotesis:
        st.header("Hipotesis")

        st.write("Pilih jenis hipotesis untuk uji pooled t-test:")

        hipotesis_pooled = st.radio(
        "Jenis Uji:",
        [
            "Dua Arah (Two-Tailed)",
            "Satu Arah Kanan (Right-Tailed)",
            "Satu Arah Kiri (Left-Tailed)"
        ],
        key="hipotesis_pooled"
    )

        if hipotesis_pooled == "Dua Arah (Two-Tailed)":
            st.latex(r"H_0 : \mu_1 = \mu_2")
            st.latex(r"H_1 : \mu_1 \neq \mu_2")
    
        elif hipotesis_pooled == "Satu Arah Kanan (Right-Tailed)":
            st.latex(r"H_0 : \mu_1 \le \mu_2")
            st.latex(r"H_1 : \mu_1 > \mu_2")
    
        elif hipotesis_pooled == "Satu Arah Kiri (Left-Tailed)":
            st.latex(r"H_0 : \mu_1 \ge \mu_2")
            st.latex(r"H_1 : \mu_1 < \mu_2")


    
    with tab_rumus:
        st.header("Rumus")

        st.latex(r"""
    t = \frac{\bar{X}_1 - \bar{X}_2}{S_p \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}
    """)

        st.latex(r"""
    S_p = \sqrt{\frac{(n_1-1)S_1^2 + (n_2-1)S_2^2}{n_1+n_2-2}}
    """)

        st.latex(r"""
    df = n_1 + n_2 - 2
    """)

        st.subheader("Penjelasan Parameter")

        st.markdown("""
    •  \\($\\bar{X}_1$\\) dan \\($\\bar{X}_2$\\)  
    Rata-rata dari sampel 1 dan sampel 2.

    •  \\($S_1^2$\\) dan \\($S_2^2$\\)  
    Varians sampel 1 dan sampel 2. Menggambarkan tingkat penyebaran data dari masing-masing sampel.

    •  \\($n_1$\\) dan \\($n_2$\\)  
    Jumlah anggota sampel 1 dan sampel 2.

    •  \\($S_p^2$\\) — Pooled Variance  
    Merupakan rata-rata tertimbang varians dua sampel ketika diasumsikan varians populasi sama.

    •  \\($S_p$\\) — Pooled Standard Deviation  
    Akar dari pooled variance. Mengestimasi standar deviasi gabungan kedua sampel.

    •  Statistik Uji \\(t\\)  
    Mengukur seberapa besar perbedaan dua rata-rata dibandingkan dengan variabilitas gabungan dan ukuran sampel.

    •  \\(df\\) Derajat Kebebasan  
    Digunakan untuk menentukan nilai kritis t dan p-value.

    •  p-value  
    Probabilitas mendapatkan nilai t setidaknya sebesar yang dihitung, jika hipotesis nol benar.
    """)

    with tab_parameter:
        st.header("Parameter")
        st.write("""
        Parameter:
        1. x̄₁, x̄₂ = rata-rata tiap sampel
        2. s₁², s₂² = varians tiap sampel
        3. n₁, n₂ = ukuran sampel
        4. df = n₁ + n₂ − 2
        5. α dan arah H1
        """)

    with tab_contoh:
        st.header("Contoh Singkat")
        st.write("""
        Misal:
        x̄₁=20, s₁²=4, n₁=15
        x̄₂=16, s₂²=3, n₂=12
        
        1. Hipotesis
        H₀: μ₁ = μ₂\n
        H₁: μ₁ ≠ μ₂
        
        2. Langkah Singkat
        Hitung pooled variance → sp ≈ 1.887\n
        t hitung ≈ 5.48\n
        df = n₁ + n₂ − 2 = 25\n
        t kritis (α=0.05 dua arah, df=25) = ±2.060
        
        3. Keputusan
        5.48 melebihi t kritis.
        ➡ Tolak H₀
        """)

    with tab_kalkulasi:
        st.header("Kalkulasi Interaktif (Masukkan Data)")
        st.write("Masukkan data sampel 1 dan sampel 2 (dipisahkan koma).")

        data1_input = st.text_area("Sampel 1 (misal: 10,12,9,11,13)", value="10,12,9,11,13")
        data2_input = st.text_area("Sampel 2 (misal: 8,9,7,10,6)", value="8,9,7,10,6")

        alpha_pooled = st.number_input("Taraf Signifikansi (α):", 0.01, 0.10, 0.05, step=0.01, key="alpha_pooled")

        # ambil jenis hipotesis dari tab_hipotesis
        hip = st.session_state.hipotesis_pooled  
    
        if st.button("Hitung Pooled t-test"):
            try:
                sample1 = np.array([float(x) for x in data1_input.split(",")])
                sample2 = np.array([float(x) for x in data2_input.split(",")])
    
                n1, n2 = len(sample1), len(sample2)
                mean1, mean2 = np.mean(sample1), np.mean(sample2)
                var1, var2 = np.var(sample1, ddof=1), np.var(sample2, ddof=1)
    
                sp = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    
                t_stat = (mean1 - mean2) / (sp * np.sqrt(1/n1 + 1/n2))
                df = n1 + n2 - 2
    
                # -------------------------
                #  HITUNG p-value BERDASAR JENIS UJI
                # -------------------------
                if hip == "Dua Arah (Two-Tailed)":
                    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))
                    t_crit = stats.t.ppf(1 - alpha_pooled/2, df)
    
                elif hip == "Satu Arah Kanan (Right-Tailed)":
                    p_value = 1 - stats.t.cdf(t_stat, df)
                    t_crit = stats.t.ppf(1 - alpha_pooled, df)
    
                else:  # Satu Arah Kiri
                    p_value = stats.t.cdf(t_stat, df)
                    t_crit = stats.t.ppf(alpha_pooled, df)
    
                # Simpan
                st.session_state.t_stat_pooled = t_stat
                st.session_state.t_crit_pooled = t_crit
                st.session_state.df_pooled = df
                st.session_state.mean_diff_pooled = mean1 - mean2
                st.session_state.sp_pooled = sp
                st.session_state.p_value_pooled = p_value
    
                st.success("Perhitungan selesai! Silakan buka tab 'Hasil & Kesimpulan'.")
            except:
                st.error("Format data salah. Pastikan hanya angka dan koma.")

    with tab_kriteria_uji:
        st.header("Kriteria dan Hasil Uji")

        if st.session_state.df_pooled > 0 and st.session_state.p_value_pooled is not None:
            colA, colB, colC, colD = st.columns(4)
            colA.metric("Mean1 - Mean2", f"{st.session_state.mean_diff_pooled:.4f}")
            colB.metric("t-hitung", f"{st.session_state.t_stat_pooled:.4f}")
            colC.metric("t-kritis", f"{st.session_state.t_crit_pooled:.4f}")
            colD.metric("p-value", f"{st.session_state.p_value_pooled:.6f}")

            st.write(f"Degree of Freedom (df): {st.session_state.df_pooled}")
            st.write(f"Pooled Std Dev (Sp): {st.session_state.sp_pooled:.4f}")

            st.markdown("---")
            st.subheader("Keputusan")

            alpha_val = st.session_state.get("alpha_pooled", alpha_pooled)

            if st.session_state.p_value_pooled < alpha_val:
                st.error(f"Tolak H0 (p-value {st.session_state.p_value_pooled:.6f} < {alpha_val})")
                st.write("Kesimpulan: Terdapat perbedaan yang signifikan antara kedua sampel.")
                st.write(f"Catatan: |t-hitung| ({abs(st.session_state.t_stat_pooled):.4f}) > t-kritis ({st.session_state.t_crit_pooled:.4f})")
            else:
                st.success(f"Gagal Tolak H0 (p-value {st.session_state.p_value_pooled:.6f} > {alpha_val})")
                st.write("Kesimpulan: Tidak cukup bukti untuk menyatakan adanya perbedaan signifikan.")
                st.write(f"Catatan: |t-hitung| ({abs(st.session_state.t_stat_pooled):.4f}) < t-kritis ({st.session_state.t_crit_pooled:.4f})")
        else:
            st.info("Belum ada data. Silakan masukkan data di tab 'Input Data & Hitung' dan klik tombol Hitung.")

    with tab_flowchart:
        st.header("Flowchart")
        st.write("Flowchart referensi untuk Uji Rata-rata 2 Sampel Independen (Pooled t-test)")
        url = "https://drive.google.com/file/d/1jwZlDKd3jswVA4L-fyWBou5rI6sB7uTv/preview"
        st.components.v1.iframe(url, width=800, height=1000)
        
# 6) Welch t-test (varians tidak sama)
elif menu == "Uji Rata-rata 2 Sampel Independen (Welch t-test)":

    st.title("Uji Rata-rata Dua Sampel Independen (Welch t-test)")
    st.write("Digunakan untuk membandingkan rata-rata dua populasi yang independen dengan *asumsi varians TIDAK sama*.")

    # Membuat Tabs sesuai struktur yang diminta
    tab_penjelasan, tab_hipotesis, tab_rumus, tab_parameter, tab_contoh, tab_kalkulasi, tab_kriteria_uji, tab_flowchart = st.tabs([
        "Konsep",
        "Hipotesis",
        "Rumus", "Parameter",
        "Contoh Perhitungan Singkat",
        "Kalkulasi",
        "Kriteria Uji", "Flowchart"
    ])

    with tab_penjelasan:
        st.header("Penjelasan")
        st.write("""
        Tujuan:
        Membandingkan rata-rata dua populasi ketika varians berbeda.
        Kapan Digunakan:
        •	Varians kedua sampel berbeda (hasil F-test).
        •	Dua sampel independen.
        Langkah Perhitungan:
        1.	Hitung rata-rata dan varians masing-masing sampel.
        2.	Hitung standard error tanpa menggabungkan varians.
        3.	Hitung nilai uji t.
        4.	Hitung derajat bebas menggunakan pendekatan Welch.
        5.	Ambil keputusan berdasarkan t kritis.
        Keputusan:
        Jika nilai t melewati batas → tolak H0.
        """)
        st.info("Syarat: Data berdistribusi normal, kedua kelompok data tidak saling berhubungan (independen).")

    with tab_hipotesis:
        st.header("Hipotesis")
        st.write("Hipotesis dua arah (Two-tailed):")
        st.latex(r"H_0 : \mu_1 = \mu_2")
        st.latex(r"H_1 : \mu_1 \neq \mu_2")
        st.write("Atau selisih rata-rata:")
        st.latex(r"H_0 : \mu_1 - \mu_2 = 0")
        st.latex(r"H_1 : \mu_1 - \mu_2 \neq 0")
        st.write("Lower-tail Test")
        st.latex(r"H_0: \mu_1 \geq \mu_2 \quad")
        st.latex(r"H_1: \mu_1 < \mu_2 \quad")
        st.write("Upper-tail Test")
        st.latex(r"H_0: \mu_1 \leq \mu_2 \quad")
        st.latex(r"H_1: \mu_1 > \mu_2 \quad")

        
    with tab_rumus:
        st.header("Rumus")
        
        st.markdown("*1. Hitung Statistik Uji $t'$:*")
        # Rumus sesuai gambar
        st.latex(r"t' = \frac{(\bar{x}_1 - \bar{x}_2)}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}")
        st.markdown(""" 
        * $\\bar{x}$ = rata-rata sampel 
        * $s^2$ = varians sampel
        * $n$ = jumlah sampel""")

        st.markdown("*2. Hitung Derajat Bebas (df) - Rumus Welch-Satterthwaite:*")
        # Rumus df yang kompleks sesuai gambar
        st.latex(r"""
        df = \frac{\left( \frac{s_1^2}{n_1} + \frac{s_2^2}{n_2} \right)^2}
        { \frac{\left( \frac{s_1^2}{n_1} \right)^2}{n_1 - 1} + \frac{\left( \frac{s_2^2}{n_2} \right)^2}{n_2 - 1} }
        """)
        st.markdown("Nilai $df$ ini biasanya berbentuk desimal dan tidak harus bulat.")

    with tab_parameter:
        st.header("Parameter")
        st.write("""
        Parameter:
        1. x̄₁, x̄₂ = rata-rata
        2. s₁², s₂² = varians
        3. n₁, n₂ = ukuran sampel
        4. df (menggunakan rumus Welch)
        5. α dan alternatif
        """)

    with tab_contoh:
        st.header("Contoh Perhitungan")
        st.write("""
        Misal: x̄₁=8, s₁²=4, n₁=10 ; x̄₂=6, s₂²=9, n₂=12
        
        1. Hipotesis
        H₀: μ₁ = μ₂\n
        H₁: μ₁ ≠ μ₂
        
        2. Langkah Singkat
        t hitung ≈ 1.87\n
        df (Welch) ≈ 19\n
        t kritis (α=0.05 dua arah, df≈19) = ±2.093
        
        3. Keputusan
        1.87 < kritis → tidak masuk daerah kritis.
        ➡ Gagal tolak H₀
        """)
        
   
    with tab_kalkulasi:
        st.header("Kalkulasi Interaktif (Masukkan Data)")
        st.warning("Pastikan data dipisahkan dengan koma (contoh: 10, 20, 30).")

        col1, col2 = st.columns(2)
        with col1:
            x1_input = st.text_area("Data Sampel 1 ($X_1$)")
        with col2:
            x2_input = st.text_area("Data Sampel 2 ($X_2$)")
        
        alpha_welch = st.number_input("Taraf Signifikansi (alpha):", 0.01, 0.20, 0.05, step=0.01, key="alpha_welch")

        jenis_uji = st.selectbox("Pilih Jenis Uji:",["Two Tail", "Upper Tail", "Lower Tail"])

        if st.button("Hitung Welch t-test"):
            try:
                # 1. Parsing Data
                data1 = np.array([float(x) for x in x1_input.split(",")])
                data2 = np.array([float(x) for x in x2_input.split(",")])

                # 2. Hitung Statistik Deskriptif
                n1, n2 = len(data1), len(data2)
                mean1, mean2 = np.mean(data1), np.mean(data2)
                # ddof=1 untuk varians sampel (s^2)
                var1, var2 = np.var(data1, ddof=1), np.var(data2, ddof=1)

                # Validasi jumlah data minimal
                if n1 < 2 or n2 < 2:
                    st.error("Setiap sampel minimal harus memiliki 2 data!")
                else:
                    # 3. Hitung t-hitung (t') sesuai rumus gambar
                    # Pembilang
                    numerator_t = mean1 - mean2
                    # Penyebut (Standard Error)
                    se_sq = (var1 / n1) + (var2 / n2)
                    se = np.sqrt(se_sq)
                    
                    t_stat = numerator_t / se

                    # 4. Hitung Derajat Bebas (df) Satterthwaite sesuai gambar
                    # Pembilang df
                    df_num = se_sq**2
                    # Penyebut df
                    term1 = ((var1 / n1)**2) / (n1 - 1)
                    term2 = ((var2 / n2)**2) / (n2 - 1)
                    df_den = term1 + term2
                    
                    df_welch = df_num / df_den

                    if jenis_uji == "Two Tail":
                        # Two-tailed: P-value dikali 2
                        p_val = 2 * (1 - stats.t.cdf(abs(t_stat), df_welch))
                        t_crit = stats.t.ppf(1 - alpha_welch/2, df_welch) # Positif
                        crit_label = f"± {t_crit:.4f}"
                        
                    elif jenis_uji == "Lower Tail":
                        # Lower-tailed: Area di kiri kurva
                        p_val = stats.t.cdf(t_stat, df_welch)
                        t_crit = stats.t.ppf(alpha_welch, df_welch) # Negatif
                        crit_label = f"{t_crit:.4f}"
                        
                    else: # Upper Tail
                        # Upper-tailed: Area di kanan kurva
                        p_val = 1 - stats.t.cdf(t_stat, df_welch)
                        t_crit = stats.t.ppf(1 - alpha_welch, df_welch) # Positif
                        crit_label = f"{t_crit:.4f}"

                    # Simpan ke Session State agar bisa dibaca di tab Hasil
                    st.session_state.res_welch = {
                        "mean1": mean1, "mean2": mean2,
                        "var1": var1, "var2": var2,
                        "n1": n1, "n2": n2,
                        "t_stat": t_stat,
                        "df": df_welch,
                        "p_val": p_val,
                        "t_crit": t_crit,
                        "crit_label": crit_label,
                        "jenis_uji": jenis_uji,
                        "valid": True
                    }
                    st.success("Perhitungan selesai! Silakan cek tab 'Kriteria uji dan Keputusan'.")

            except ValueError:
                st.error("Format data salah. Pastikan hanya memasukkan angka dipisah koma.")

    
    with tab_kriteria_uji:
        st.header("Kriteria dan Hasil Uji")

        # Cek apakah hasil sudah ada di session state
        if "res_welch" in st.session_state and st.session_state.res_welch["valid"]:
            res = st.session_state.res_welch
            jenis = res['jenis_uji']
            alpha = st.session_state.alpha_welch
            
            # Tampilan Metric Utama
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Jenis Uji", jenis_uji)
            c2.metric("t-hitung", f"{res['t_stat']:.4f}")
            c3.metric("p-value", f"{res['p_val']:.4f}")
            c4.metric("Nilai Kritis", res['crit_label'])

            st.markdown("---")
            st.subheader("Detail Statistik")
            # Menampilkan tabel ringkasan
            summary_data = {
                "Sampel": ["Kelompok 1", "Kelompok 2"],
                "Jumlah (n)": [res['n1'], res['n2']],
                "Rata-rata": [res['mean1'], res['mean2']],
                "Varians ($s^2$)": [res['var1'], res['var2']]
            }
            st.table(pd.DataFrame(summary_data))

            st.markdown("---")

          # --- MENAMPILKAN KRITERIA UJI (Format Baru) ---
            st.markdown("---")
            st.subheader("Kriteria Penolakan H0")
            
            # Mengambil variabel dari hasil perhitungan (session state)
            jenis = res['jenis_uji']
            t_crit_val = res['t_crit']
            alpha_val = st.session_state.alpha_welch

            # Logika Tampilan menggunakan f-string (rf"")
            if jenis == "Two Tail":
                # Ambil nilai mutlak untuk tampilan uji dua arah
                tc_abs = abs(t_crit_val)
                
                st.markdown(rf"""
                *Two-tail Test (Uji Dua Arah)* $H_1: \mu_1 \neq \mu_2$
                
                Berdasarkan Nilai Kritis:
                * Tolak $H_0$ jika $|t'_{{hitung}}| > {tc_abs:.4f}$
                * Gagal tolak $H_0$ jika $|t'_{{hitung}}| \le {tc_abs:.4f}$
                
                Berdasarkan P-value:
                * Tolak $H_0$ jika $p\text{{-value}} < \alpha$ ({alpha_val})
                """)

            elif jenis == "Upper Tail":
                st.markdown(rf"""
                *Upper-tail (Uji Pihak Kanan)* $H_1: \mu_1 > \mu_2$
                
                Berdasarkan Nilai Kritis:
                * Tolak $H_0$ jika $t'_{{hitung}} > {t_crit_val:.4f}$
                * Gagal tolak $H_0$ jika $t'_{{hitung}} \le {t_crit_val:.4f}$
                
                Berdasarkan P-value:
                * Tolak $H_0$ jika $p\text{{-value}} < \alpha$ ({alpha_val})
                """)

            elif jenis == "Lower Tail":
                st.markdown(rf"""
                *Lower-tail (Uji Pihak Kiri)* $H_1: \mu_1 < \mu_2$
                
                Berdasarkan Nilai Kritis:
                * Tolak $H_0$ jika $t'_{{hitung}} < {t_crit_val:.4f}$
                * Gagal tolak $H_0$ jika $t'_{{hitung}} \ge {t_crit_val:.4f}$
                
                Berdasarkan P-value:
                * Tolak $H_0$ jika $p\text{{-value}} < \alpha$ ({alpha_val})
                """)
            
            st.markdown("---")
            st.success("*Kesimpulan:* Jika kondisi di atas terpenuhi, maka kita menolak $H_0$ dan menerima hipotesis alternatif ($H_1$).")
            st.subheader("Keputusan")
            
            # Logika Keputusan Dinamis
            tolak_h0 = False
            alasan = ""

            # Cara 1: Menggunakan P-Value (Universal)
            if res['p_val'] < alpha:
                tolak_h0 = True
                alasan = f"Karena p-value ({res['p_val']:.4f}) < Alpha ({alpha})"
            else:
                tolak_h0 = False
                alasan = f"Karena p-value ({res['p_val']:.4f}) > Alpha ({alpha})"
            
            if tolak_h0:
                st.error(f"*Keputusan: TOLAK H0*")
                st.write(alasan)
                if jenis == "Two Tail":
                    st.write("*Kesimpulan:* Ada perbedaan signifikan antara rata-rata kedua populasi.")
                elif jenis == "Upper Tail":
                    st.write("*Kesimpulan:* Rata-rata Populasi 1 LEBIH BESAR secara signifikan dari Populasi 2.")
                elif jenis == "Lower Tail":
                    st.write("*Kesimpulan:* Rata-rata Populasi 1 LEBIH KECIL secara signifikan dari Populasi 2.")
            else:
                st.success(f"*Keputusan: GAGAL TOLAK H0*")
                st.write(alasan)
                st.write("*Kesimpulan:* Tidak cukup bukti untuk mendukung hipotesis alternatif (H1).")

            # Visualisasi Posisi t-hitung (Opsional Text Based)
            st.markdown("---")
            st.write(f"*Posisi t-hitung vs Kritis:*")
            if jenis == "Two Tail":
                # Two Tailed
                val_t = abs(res['t_stat'])
                val_crit = abs(res['t_crit'])
                status = "YA (Signifikan)" if val_t > val_crit else "TIDAK (Tidak Signifikan)"
                
                st.write(f"Analisis Dua Arah (Two-Tailed):")
                st.latex(r"|t_{hitung}| > |t_{kritis}| ?")
                st.write(f"Apakah |{res['t_stat']:.4f}| > {val_crit:.4f}?")
                st.info(f"Jawab: *{status}*")

            elif jenis == "Upper Tail":
                # Upper Tailed
                status = "YA (Signifikan)" if res['t_stat'] > res['t_crit'] else "TIDAK (Tidak Signifikan)"
                
                st.write(f"Analisis Satu Arah Kanan (Upper-Tailed):")
                st.latex(r"t_{hitung} > t_{kritis} ?")
                st.write(f"Apakah {res['t_stat']:.4f} > {res['t_crit']:.4f}?")
                st.info(f"Jawab: *{status}*")

            elif jenis == "Lower Tail":
                # Lower Tailed
                status = "YA (Signifikan)" if res['t_stat'] < res['t_crit'] else "TIDAK (Tidak Signifikan)"
                
                st.write(f"Analisis Satu Arah Kiri (Lower-Tailed):")
                st.latex(r"t_{hitung} < t_{kritis} ?")
                st.write(f"Apakah {res['t_stat']:.4f} < {res['t_crit']:.4f}?")
                st.info(f"Jawab: *{status}*")
            
            else:
                st.warning("Jenis uji tidak terdeteksi. Pastikan pilihan di dropdown sesuai.")

        else:
            st.info("Belum ada data yang dihitung. Silakan input data di tab sebelumnya.")

    with tab_flowchart:
        st.header("Flowchart")
        st.write("Flowchart referensi untuk Uji Rata-rata 2 Sampel Independen (Welch t-tes)")
        url = "https://drive.google.com/file/d/1QaVAncDvluaUCUKBT1FWzgnvT9BWFLmk/preview"
        st.components.v1.iframe(url, width=800, height=1000)

# 7) Paired t-test (dependent samples)

elif menu == "Uji Rata-rata 2 Sampel Dependen (Paired t-test)":

    st.title("Uji Rata-rata Dua Sampel Dependen (Paired t-test)")
    st.write("Digunakan ketika dua data saling berpasangan (paired).")

    tab_penjelasan, tab_hipotesis, tab_rumus, tab_parameter, tab_contoh, tab_kalkulasi, tab_kriteria_uji, tab_flowchart = st.tabs([
        "Konsep",
        "Hipotesis",
        "Rumus", "Parameter",
        "Contoh Perhitungan Singkat",
        "Kalkulasi",
        "Kriteria Uji", "Flowchart"
    ])


    with tab_penjelasan:
        st.header("Penjelasan")
        st.write(""" 
        Tujuan:
        Menilai apakah terdapat perubahan/perbedaan rata-rata dari pasangan data yang saling berkaitan.
        Kapan Digunakan:
        •	Data sebelum–sesudah pada subjek yang sama.
        •	Dua kondisi pengukuran pada objek yang sama.
        Langkah Perhitungan:
        1.	Hitung selisih tiap pasangan data.
        2.	Hitung rata-rata selisih.
        3.	Hitung standar deviasi selisih.
        4.	Hitung standard error selisih.
        5.	Hitung nilai uji t.
        6.	Gunakan derajat bebas (n − 1).
        Keputusan:
        Jika nilai t signifikan → ada perubahan → tolak H0.
        """)

    with tab_hipotesis:
        st.header("Hipotesis Uji")
        st.subheader("Two-tail Test")
        st.latex(r"H_0 : \mu_D = 0")
        st.latex(r"H_1 : \mu_D \neq 0")
        st.subheader("Upper-tail Test")
        st.latex(r"H_0 : \mu_D \leq 0")
        st.latex(r"H_1 : \mu_D > 0")
        st.subheader("Lower-tail Test")
        st.latex(r"H_0 : \mu_D \geq 0")
        st.latex(r"H_1 : \mu_D < 0")
        st.write("Dengan:")
        st.write("• D = selisih setiap data (X1 - X2)")
        st.write("• μD = rata-rata selisih populasi")

                
    with tab_rumus:
        st.header("Rumus Paired t-test")
        
        st.write("1. Selisih tiap pasangan (d) ")
        st.latex(r""" d_i = X_{1i} - X_{2i} """)
        st.markdown(r"$X_{1i}$ = Nilai ke(i) pada data kondisi pertama")
        st.markdown(r"$X_{2i}$ = Nilai ke(i) pada data kondisi kedua")
        
        st.write("2.  Rata-rata selisih")
        st.latex(r"""\bar{X}_d = \frac{\sum d_i}{n}""")
        st.markdown(r"$\bar{X}_d$ = Rata rata dari selisih dua data""")
        st.markdown("$$\\sum d_i$$ = jumlah dari seluruh nilai selisih")
        st.markdown("${n}$ = jumlah kedua data (n1 + n2)")
        
        st.write("3. Simpangan baku selisih")
        st.latex(r""" s_d = \sqrt{\frac{\sum(d_i - \bar{X}_d)^2}{n-1}} """)
        st.markdown(r"$\bar{X}_d$ = Rata rata dari selisih dua data""")
        st.markdown(r"$d_i$ = nilai $d_i$ ke(i)""")
        st.markdown("${n}$ = jumlah kedua data (n1 + n2)")
        
        st.write("4. Statistik uji t")
        st.latex(r""" t = \frac{\bar{X}_d - \mu_0}{s_d / \sqrt{n}} """)
        st.markdown(r"$\bar{X}_d$ = Rata rata dari selisih dua data""")
        st.markdown(r"$\mu_0$ = Rata rata yang di hipotesiskan dalam H0 (biasanya bernilai 0)")
        st.markdown(r"$s_d$ = Simpangan Baku selisih")
        st.markdown("${n}$ = jumlah kedua data (n1 + n2)")

        st.write("5. Derajat bebas")
        st.latex(r""" df = n - 1 """)
        st.markdown("${n}$ = jumlah kedua data (n1 + n2)")

    with tab_parameter:
        st.header("Parameter")
        st.write("""
        Parameter:
        1. dᵢ = selisih tiap pasangan (X − Y)
        2. d̄ = rata-rata selisih
        3. sd = standar deviasi selisih
        4. n = jumlah pasangan
        5. df = n − 1
        6. α & bentuk H1
        """)

    with tab_contoh:
        st.header("Contoh Perhitungan singkat")
        st.write("""
        Misal:
        Selisih dᵢ → d̄ = 0.1, sd = 8.034, n = 10
        
        1. Hipotesis
        H₀: μᵈ = 0 (tidak ada perbedaan)
        H₁: μᵈ ≠ 0
        
        2. Langkah Singkat
        t hitung = 0.039
        df = 9
        t kritis (df=9, α=0.05 dua arah) = ±2.262
        
        3. Keputusan
        0.039 jauh dari wilayah kritis.
        ➡ Gagal tolak H₀.
        """)

    with tab_kalkulasi:
        st.header("Kalkulasi Interaktif (Masukkan Data)")
        st.write("Masukkan data X1 dan X2 (dipisahkan koma).")

        x1_input = st.text_area("Data X1 (misal: 10,12,9,15,11)")
        x2_input = st.text_area("Data X2 (misal: 8,11,7,14,10)")
        alpha_paired = st.number_input("Taraf Signifikansi (α):", 0.01, 0.10, 0.05, step=0.01, key="alpha_paired")
        jenis_uji = st.selectbox("Pilih Jenis Uji:",["Two Tail","Upper Tail", "Lower Tail"])

        if st.button("Hitung Uji t Paired"):
            try:
                # Parsing input
                x1_arr = np.array([float(i) for i in x1_input.split(",")])
                x2_arr = np.array([float(i) for i in x2_input.split(",")])

                if len(x1_arr) != len(x2_arr):
                    st.error("Error: Jumlah data X1 dan X2 harus sama!")
                else:
                    # Perhitungan
                    D_arr = x1_arr - x2_arr
                    n_calc = len(D_arr)
                    df_calc = n_calc - 1
                    
                    mean_D_calc = np.mean(D_arr)
                    sd_D_calc = np.std(D_arr, ddof=1)
                    
                    # Hindari pembagian dengan nol
                    if sd_D_calc == 0:
                        st.warning("Standar deviasi selisih adalah 0, t-hitung tidak terdefinisi.")
                    else:
                        t_stat_calc = mean_D_calc / (sd_D_calc / np.sqrt(n_calc))
                        
                        # Hitung P-Value sesuai jenis uji
                        if jenis_uji == "Two Tail":
                            p_val_calc = 2 * (1 - stats.t.cdf(abs(t_stat_calc), df_calc))
                            t_crit_calc = stats.t.ppf(1 - alpha_paired/2, df_calc)
                        
                        elif jenis_uji == "Upper Tail":
                            p_val_calc = 1 - stats.t.cdf(t_stat_calc, df_calc)
                            t_crit_calc = stats.t.ppf(1 - alpha_paired, df_calc)
                        
                        elif jenis_uji == "Lower Tail":
                            p_val_calc = stats.t.cdf(t_stat_calc, df_calc)
                            t_crit_calc = stats.t.ppf(alpha_paired, df_calc)

                        # Simpan ke Session State
                        st.session_state.t_stat_paired = t_stat_calc
                        st.session_state.t_crit_paired = t_crit_calc
                        st.session_state.df_calc = df_calc
                        st.session_state.mean_d_paired = mean_D_calc
                        st.session_state.sd_d_paired = sd_D_calc
                        st.session_state.p_value_paired = p_val_calc
                        
                        st.success("Perhitungan selesai! Silakan buka tab 'Hasil & Kesimpulan'.")

                        #Simpan untuk tab 6
                        st.session_state.jenis_uji = jenis_uji
                        
            except ValueError:
                st.error("Format data salah. Pastikan hanya angka dan koma.")

    with tab_kriteria_uji:
        st.header("Kriteria dan Hasil Uji")
        
        # Cek apakah perhitungan sudah dilakukan (df > 0)
        if st.session_state.df_calc > 0 and st.session_state.p_value_paired is not None:
            colA, colB, colC, colD = st.columns(4)
            colA.metric("Rata-rata Selisih", f"{st.session_state.mean_d_paired:.4f}")
            colB.metric("t-hitung", f"{st.session_state.t_stat_paired:.4f}")
            colC.metric("t-kritis", f"{st.session_state.t_crit_paired:.4f}")
            colD.metric("p-value", f"{st.session_state.p_value_paired:.6f}")
            
            st.write(f"Degree of Freedom (df): *{st.session_state.df_calc}*")
            st.write(f"Standar Deviasi Selisih: *{st.session_state.sd_d_paired:.4f}*")
            
            st.markdown("---")
            st.subheader("Keputusan")
            
             # ambil nilai
            t_stat = st.session_state.t_stat_paired
            t_crit = st.session_state.t_crit_paired
            p_value = st.session_state.p_value_paired
            alpha_val = st.session_state.alpha_paired
            jenis = st.session_state.jenis_uji
        
            # Two Tail
            if jenis == "Two Tail":
                if p_value < alpha_val and abs(t_stat) > t_crit:
                    st.error(f"*Tolak H0* (p-value {p_value:.6f} < α {alpha_val})")
                    st.write(f"|t-hitung| ({abs(t_stat):.4f}) > t-kritis ({t_crit:.4f})")
                else:
                    st.success(f"*Gagal Tolak H0* (p-value {p_value:.6f} ≥ α {alpha_val})")
                    st.write(f"|t-hitung| ({abs(t_stat):.4f}) ≤ t-kritis ({t_crit:.4f})")
        
            # Upper Tail
            elif jenis == "Upper Tail":
                if p_value < alpha_val and t_stat > t_crit:
                    st.error(f"*Tolak H0* (p-value {p_value:.6f} < α {alpha_val})")
                    st.write(f"t-hitung ({t_stat:.4f}) > t-kritis ({t_crit:.4f})")
                else:
                    st.success(f"*Gagal Tolak H0* (p-value {p_value:.6f} ≥ α {alpha_val})")
                    st.write(f"t-hitung ({t_stat:.4f}) ≤ t-kritis ({t_crit:.4f})")

            # Lower Tail
            elif jenis == "Lower Tail":
                if p_value < alpha_val and t_stat < t_crit:
                    st.error(f"*Tolak H0* (p-value {p_value:.6f} < α {alpha_val})")
                    st.write(f"t-hitung ({t_stat:.4f}) < t-kritis ({t_crit:.4f})")
                else:
                    st.success(f"*Gagal Tolak H0* (p-value {p_value:.6f} ≥ α {alpha_val})")
                    st.write(f"t-hitung ({t_stat:.4f}) ≥ t-kritis ({t_crit:.4f})")

        else:
            st.info("Belum ada data. Silakan masukkan data di tab 'Hitung (Input)' dan klik tombol Hitung.")

    with tab_flowchart:
        st.header("Flowchart")
        st.write("Flowchart referensi untuk Uji Rata-rata 2 Sampel Dependen (Paired t-test)")
        url = "https://drive.google.com/file/d/1Py2T6DLhHoGteB8rlgC3cmT5ipgB-KlN/preview"
        st.components.v1.iframe(url, width=800, height=1000)
      
