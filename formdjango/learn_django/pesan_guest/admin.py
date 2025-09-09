from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')  # Menampilkan kolom yang ingin ditampilkan di admin
    search_fields = ('name', 'email', 'subject')  # Menambahkan fitur pencarian
    list_filter = ('created_at',)  # Menambahkan filter berdasarkan tanggal
