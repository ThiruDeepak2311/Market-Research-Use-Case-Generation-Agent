import json
from fpdf import FPDF


class PDFReport(FPDF):
    def header(self):
        if self.page_no() == 1:
            return  # No header on the first page (cover page)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, "AI & GenAI Use Case Report", align="C", ln=True)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_cover_page(self, title, subtitle, date):
        self.add_page()
        self.set_font("Arial", "B", 20)
        self.cell(0, 10, title, ln=True, align="C")
        self.ln(10)
        self.set_font("Arial", "I", 14)
        self.cell(0, 10, subtitle, ln=True, align="C")
        self.ln(20)
        self.set_font("Arial", "", 12)
        self.cell(0, 10, f"Date: {date}", ln=True, align="C")
        self.ln(50)
        self.set_font("Arial", "I", 12)
        self.cell(0, 10, "Generated by AI Use Case Generator", align="C")

    def add_section_title(self, title):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, title, ln=True, align="L")
        self.ln(5)

    def add_paragraph(self, text):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, text)
        self.ln()

    def add_bullet_point(self, text):
        self.set_font("Arial", "", 12)
        self.cell(10)  # Indentation
        self.cell(0, 10, f"- {text}", ln=True)

    def add_hyperlink(self, text, url):
        self.set_font("Arial", "U", 12)
        self.set_text_color(0, 0, 255)
        self.cell(0, 10, text, link=url, ln=True)
        self.set_text_color(0, 0, 0)


def generate_report():
    try:
        pdf = PDFReport()

        # Cover Page
        pdf.add_cover_page(
            title="AI & GenAI Use Case Report",
            subtitle="Industry Trends, Use Cases, and Resource Insights",
            date="January 2025"
        )

        # Load content from files
        with open("research_output.json", "r") as file:
            research_data = json.load(file)

        with open("use_cases.md", "r") as file:
            use_cases = file.read()

        with open("resources.md", "r") as file:
            resources = file.read()

        # Industry Trends
        pdf.add_page()
        pdf.add_section_title("Industry Trends")
        for trend in research_data.get("industry_trends", []):
            pdf.add_bullet_point(trend)

        # Competitors
        pdf.add_section_title("Competitors")
        for competitor in research_data.get("competitors", []):
            pdf.add_bullet_point(competitor)

        # AI Insights
        pdf.add_section_title("AI Insights")
        pdf.add_paragraph(research_data.get("ai_insights", ""))

        # Use Cases
        pdf.add_section_title("AI/GenAI Use Cases")
        pdf.add_paragraph(use_cases)

        # Relevant Datasets
        pdf.add_section_title("Relevant Datasets")
        for line in resources.split("\n"):
            if line.startswith("-"):
                parts = line.split(" - ")
                if len(parts) == 2:
                    dataset_name, url = parts
                    pdf.add_hyperlink(dataset_name.strip(), url.strip())
                else:
                    pdf.add_paragraph(line.strip())
            else:
                pdf.add_paragraph(line.strip())

        # Save PDF
        pdf.output("GenAI_Summary_Report.pdf")
        print("Report generated successfully: GenAI_Summary_Report.pdf")

    except Exception as e:
        print(f"Error generating report: {str(e)}")


if __name__ == "__main__":
    generate_report()
