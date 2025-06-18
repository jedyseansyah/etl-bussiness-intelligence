import csv
from django.core.management.base import BaseCommand
from uasbi.models import FactCampaign, FactCustomer, FactSales
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Import data from OLAP CSV files'

    def handle(self, *args, **kwargs):
        # Hapus data lama (jika ada saat akan import baru)
        self.stdout.write("Menghapus data lama...")
        FactCampaign.objects.all().delete()
        FactCustomer.objects.all().delete()
        FactSales.objects.all().delete()

        # Path ke file-file CSV
        campaign_csv_path = os.path.join(settings.BASE_DIR, 'OLAP_data_factcampaign.csv')
        customer_csv_path = os.path.join(settings.BASE_DIR, 'OLAP_data_factcustomer.csv')
        sales_csv_path = os.path.join(settings.BASE_DIR, 'OLAP_data_factsales.csv')

        # Impor FactCampaign
        self.stdout.write("Mengimpor data FactCampaign...")
        try:
            with open(campaign_csv_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    FactCampaign.objects.create(
                        product=row['Product'],
                        year=int(row['Year']),
                        month=int(row['Month']),
                        units_sold=int(row['UnitsSold']),
                        revenue=float(row['Revenue']),
                        operating_profit=float(row['OperatingProfit']),
                        roi=row['Roi']
                    )
            self.stdout.write(self.style.SUCCESS('Data FactCampaign berhasil diimpor.'))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File {campaign_csv_path} tidak ditemukan.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Terjadi error saat impor FactCampaign: {e}'))


        # Impor FactCustomer
        self.stdout.write("Mengimpor data FactCustomer...")
        try:
            with open(customer_csv_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    FactCustomer.objects.create(
                        year=int(row['Year']),
                        month=int(row['Month']),
                        state=row['State'],
                        city=row['City'],
                        product=row['Product'],
                        units_sold=int(row['UnitsSold']),
                        revenue=float(row['Revenue']),
                        operating_profit=float(row['OperatingProfit'])
                    )
            self.stdout.write(self.style.SUCCESS('Data FactCustomer berhasil diimpor.'))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File {customer_csv_path} tidak ditemukan.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Terjadi error saat impor FactCustomer: {e}'))


        # Impor FactSales
        self.stdout.write("Mengimpor data FactSales...")
        try:
            with open(sales_csv_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    FactSales.objects.create(
                        product=row['Product'],
                        year=int(row['Year']),
                        month=int(row['Month']),
                        retailer=row['Retailer'],
                        sales_method=row['SalesMethod'],
                        units_sold=int(row['UnitsSold']),
                        revenue=float(row['Revenue']),
                        operating_profit=float(row['OperatingProfit'])
                    )
            self.stdout.write(self.style.SUCCESS('Data FactSales berhasil diimpor.'))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File {sales_csv_path} tidak ditemukan.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Terjadi error saat impor FactSales: {e}'))

        self.stdout.write(self.style.SUCCESS('Semua proses impor telah selesai.'))