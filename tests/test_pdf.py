from src.pdf_generator import create_pdf


transcript = """
[00:00 - 00:05] The project meeting started.
[00:05 - 00:12] The team discussed the deadline.
"""


analysis = """
1. Summary

The team discussed the project deadline.

2. Key Discussion Points

The project deadline was the main topic.

3. Decisions or Conclusions

The deadline was confirmed.

4. Action Items

The team will complete the remaining work.
"""


output_path = "data/output/meetmind_report.pdf"


create_pdf(
    transcript,
    analysis,
    output_path
)


print("PDF created successfully!")
print("Saved to:", output_path)