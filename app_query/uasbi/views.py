from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.db.models import Sum
from .models import FactCampaign, FactCustomer, FactSales
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

# Create your views here.
def index(request):
    return render(request, 'index.html')

def tampil_fact_campaign(request):
    semua_campaign = FactCampaign.objects.all()
    konteks = {
        'judul_halaman': 'Data Fact Campaign',
        'campaigns': semua_campaign,
    }
    return render(request, 'factcampaign.html', konteks)

def tampil_fact_campaign_chart(request):
    chart_base64 = None
    try:
        # 1. Ambil semua data campaign
        campaign_data = FactCampaign.objects.all().values()

        if campaign_data:
            # 2. Konversi ke DataFrame Pandas
            df = pd.DataFrame.from_records(campaign_data)

            # 3. Agregasi data: Jumlahkan operating_profit berdasarkan tahun dan bulan
            grouped_data = df.groupby(['year', 'month'])['operating_profit'].sum().reset_index()

            # Buat nama bulan untuk sumbu X
            month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun', 
                         7: 'Jul', 8: 'Agu', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'}
            grouped_data['month_name'] = grouped_data['month'].map(month_map)
            
            # Urutkan berdasarkan bulan secara benar
            grouped_data['month'] = pd.Categorical(grouped_data['month_name'], categories=month_map.values(), ordered=True)

            # 4. Membuat Grafik Garis
            plt.style.use('seaborn-v0_8-whitegrid')
            fig, ax = plt.subplots(figsize=(14, 7))

            sns.lineplot(
                data=grouped_data,
                x='month',
                y='operating_profit',
                hue='year', # Warna garis berbeda untuk setiap tahun
                palette='viridis', # Gunakan palet warna yang berbeda
                marker='o',
                ax=ax
            )

            # 5. Kustomisasi Grafik
            ax.set_title('Operating Profit per Bulan', fontsize=18)
            ax.set_xlabel('Bulan', fontsize=12)
            ax.set_ylabel('Total Operating Profit', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            ax.margins(x=0)
            plt.tight_layout()

            # 6. Simpan grafik ke buffer dan encode ke Base64
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            chart_base64 = base64.b64encode(buf.read()).decode('utf-8')
            buf.close()

    except Exception as e:
        print(f"Error creating campaign chart: {e}")

    finally:
        plt.close()

    konteks = {
        'judul_halaman': 'Visualisasi Data Campaign',
        'chart_base64': chart_base64,
        'campaign_data': FactCampaign.objects.all()
    }
    return render(request, 'factcampaign_chart.html', konteks)


def tampil_fact_customers(request):
    semua_customer = FactCustomer.objects.all()
    konteks = {
        'judul_halaman': 'Tabel Data Pelanggan',
        'customers': semua_customer,
    }
    return render(request, 'factcustomers.html', konteks)

def tampil_fact_customers_chart(request):
    chart_base64 = None
    try:
        # 1. Ambil semua data customer
        customer_data = FactCustomer.objects.all().values()

        if customer_data:
            # 2. Konversi ke DataFrame Pandas
            df = pd.DataFrame.from_records(customer_data)

            # 3. Agregasi data: Jumlahkan unit_sold berdasarkan kota dan produk
            grouped_data = df.groupby(['city', 'product'])['units_sold'].sum().reset_index()

            # 4. Membuat Grafik Batang
            plt.style.use('seaborn-v0_8-whitegrid')
            fig, ax = plt.subplots(figsize=(16, 9))

            sns.barplot(
                data=grouped_data,
                x='city',
                y='units_sold',
                hue='product', # Warna batang berbeda untuk setiap produk
                ax=ax
            )

            # 5. Kustomisasi Grafik
            ax.set_title('Total Unit Terjual per Produk di Setiap Kota', fontsize=18)
            ax.set_xlabel('Kota', fontsize=12)
            ax.set_ylabel('Total Unit Terjual', fontsize=12)
            plt.xticks(rotation=45, ha='right') # Putar label kota agar mudah dibaca
            plt.tight_layout()

            # 6. Simpan grafik ke buffer dan encode ke Base64
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            chart_base64 = base64.b64encode(buf.read()).decode('utf-8')
            buf.close()

    except Exception as e:
        print(f"Error creating customer chart: {e}")

    finally:
        plt.close()

    konteks = {
        'judul_halaman': 'Visualisasi Data Pelanggan',
        'chart_base64': chart_base64,
        # Kita juga bisa mengirimkan data tabel jika ingin menampilkannya di bawah grafik
        'customer_data': FactCustomer.objects.all(),
    }
    return render(request, 'factcustomers_chart.html', konteks)


def tampil_fact_sales(request):
    semua_sales = FactSales.objects.all()
    konteks = {
        'judul_halaman': 'Tabel Data Sales',
        'sales': semua_sales,
    }
    return render(request, 'factsales.html', konteks)

def tampil_fact_sales_chart(request):
    semua_sales = FactSales.objects.all()

    chart_base64 = None
    try:
        # 1. Filter data hanya untuk tahun 2020 dan 2021
        sales_for_chart = FactSales.objects.filter(year__in=[2020, 2021]).values()

        if sales_for_chart:
            # 2. Konversi data ke DataFrame Pandas untuk kemudahan manipulasi
            df = pd.DataFrame.from_records(sales_for_chart)
            
            # 3. Gabungkan 'product' dan 'year' untuk label yang unik di legenda
            df['product_year'] = df['product'] + ' (' + df['year'].astype(str) + ')'
            
            # Buat nama bulan untuk sumbu X yang lebih baik
            month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun', 
                         7: 'Jul', 8: 'Agu', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'}
            df['month_name'] = df['month'].map(month_map)
            
            # Urutkan berdasarkan bulan secara benar
            df['month'] = pd.Categorical(df['month_name'], categories=month_map.values(), ordered=True)

            # 4. Membuat Grafik
            plt.style.use('seaborn-v0_8-whitegrid') # Menggunakan style dari seaborn
            fig, ax = plt.subplots(figsize=(14, 7))

            sns.lineplot(
                data=df,
                x='month',
                y='units_sold',
                hue='product_year', # Garis yang berbeda untuk setiap kombinasi produk dan tahun
                marker='o', # Tambahkan titik pada setiap data point
                ax=ax
            )

            # 5. Kustomisasi Grafik
            ax.set_title('Penjualan Unit per Bulan (2020-2021)', fontsize=16)
            ax.set_xlabel('Bulan', fontsize=12)
            ax.set_ylabel('Jumlah Unit Terjual', fontsize=12)
            plt.xticks(rotation=45) # Putar label sumbu X agar tidak tumpang tindih
            ax.margins(x=0)
            plt.tight_layout() # Rapikan layout
            
            # 6. Simpan grafik ke buffer memori
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            
            # 7. Encode gambar ke Base64
            chart_base64 = base64.b64encode(buf.read()).decode('utf-8')
            buf.close()

    except Exception as e:
        print(f"Error creating chart: {e}") # Log error jika terjadi masalah

    finally:
        plt.close() # Pastikan plot ditutup untuk melepaskan memori

    konteks = {
        'judul_halaman': 'Visualisasi Data Sales',
        'sales_data': semua_sales,
        'chart_base64': chart_base64, # Kirim string Base64 ke template
    }
    return render(request, 'factsales_chart.html', konteks)