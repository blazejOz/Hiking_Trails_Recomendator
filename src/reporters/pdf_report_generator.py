from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime
import matplotlib.pyplot as plt
import tempfile
import os

from src.reporters.chart_generator import ChartGenerator



class PDFReportGenerator:
    def __init__(self, routes, weather_data, user_pref=None):
        self.routes = routes
        self.weather_data = weather_data
        self.user_pref = user_pref
        self.styles = getSampleStyleSheet()

    def _header_footer(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.drawString(30, 820, f"Raport tras turystycznych - {datetime.now().strftime('%Y-%m-%d')}")
        canvas.drawRightString(570, 820, f"Strona {doc.page}")
        canvas.restoreState()

    def generate(self, filename):
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []

        # Strona tytułowa
        elements.append(Paragraph("Raport rekomendowanych tras", self.styles['Title']))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(f"Data generowania: {datetime.now().strftime('%Y-%m-%d %H:%M')}", self.styles['Normal']))
        if self.user_pref:
            elements.append(Paragraph(f"Parametry wyszukiwania: {self.user_pref.__dict__}", self.styles['Normal']))
        elements.append(PageBreak())

        # Spis treści (prosty)
        elements.append(Paragraph("Spis treści", self.styles['Heading2']))
        elements.append(Paragraph("1. Podsumowanie", self.styles['Normal']))
        elements.append(Paragraph("2. Szczegóły tras", self.styles['Normal']))
        elements.append(Paragraph("3. Wykresy", self.styles['Normal']))
        elements.append(Paragraph("4. Tabela zbiorcza", self.styles['Normal']))
        elements.append(Paragraph("5. Aneks", self.styles['Normal']))
        elements.append(PageBreak())

        # Podsumowanie
        elements.append(Paragraph("Podsumowanie wykonawcze", self.styles['Heading2']))
        elements.append(Paragraph(f"Liczba rekomendowanych tras: {len(self.routes)}", self.styles['Normal']))
        elements.append(PageBreak())

        # Szczegóły tras
        elements.append(Paragraph("Szczegółowe opisy tras", self.styles['Heading2']))
        for route, weather in zip(self.routes, self.weather_data):
            elements.append(Paragraph(f"<b>{route.name}</b> ({route.region})", self.styles['Heading3']))
            elements.append(Paragraph(f"Długość: {route.length_km} km, Przewyższenie: {route.elevation_gain} m, Trudność: {route.difficulty}", self.styles['Normal']))
            elements.append(Paragraph(f"Typ terenu: {route.terrain_type}, Tagi: {', '.join(route.tags)}", self.styles['Normal']))
            elements.append(Paragraph(f"Pogoda: {weather.avg_temp}°C, opady: {weather.precipitation} mm, zachmurzenie: {weather.cloud_cover}%", self.styles['Normal']))
            elements.append(Spacer(1, 10))
        elements.append(PageBreak())

        # Wykresy
        elements.append(Paragraph("Wykresy porównawcze", self.styles['Heading2']))
        with tempfile.TemporaryDirectory() as tmpdir:
            bar_path = os.path.join(tmpdir, "bar_chart.png")
            pie_path = os.path.join(tmpdir, "pie_chart.png")
            ChartGenerator.bar_chart(self.routes, bar_path)
            ChartGenerator.pie_chart(self.routes, pie_path)
            from reportlab.platypus import Image
            elements.append(Paragraph("Histogram długości tras", self.styles['Heading3']))
            elements.append(Image(bar_path, width=400, height=200))
            elements.append(Paragraph("Wykres kołowy kategorii tras", self.styles['Heading3']))
            elements.append(Image(pie_path, width=300, height=300))
        elements.append(PageBreak())

        # Tabela zbiorcza
        elements.append(Paragraph("Tabela zbiorcza tras", self.styles['Heading2']))
        data = [["Nazwa", "Region", "Długość (km)", "Trudność", "Typ terenu", "Temp. (°C)", "Opady (mm)"]]
        for route, weather in zip(self.routes, self.weather_data):
            data.append([
                route.name, route.region, route.length_km, route.difficulty, route.terrain_type,
                weather.avg_temp, weather.precipitation
            ])
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONT', (0,0), (-1,0), 'Helvetica-Bold')
        ]))
        elements.append(table)
        elements.append(PageBreak())

        # Aneks
        elements.append(Paragraph("Aneks z danymi źródłowymi", self.styles['Heading2']))
        elements.append(Paragraph("Tu możesz dodać szczegółowe dane lub źródła.", self.styles['Normal']))

        doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer)