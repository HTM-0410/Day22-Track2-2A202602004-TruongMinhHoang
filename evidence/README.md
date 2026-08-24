# Minh chứng Day 22 — LangSmith + Prompt Versioning

## Kết quả đã đo

- Bước 1: 50/50 câu hỏi chạy qua RAG pipeline; knowledge base được chia thành 107 chunks và index bằng FAISS.
- Bước 2: hai prompt `truong-minh-hoang-day22-rag-v1` và `truong-minh-hoang-day22-rag-v2` đã được push rồi pull lại từ Prompt Hub. A/B routing tất định phân bổ V1=19, V2=31 trên 50 request ID.
- Bước 3: chạy đủ 50 QA qua cả V1 và V2. API LangSmith xác nhận project có ít nhất 100 root traces; giao diện Stats tại thời điểm chụp hiển thị `Trace Count = 323`.
- Bước 4: 6 case PII và 5 case JSON đều qua assertion; PII được che và JSON lỗi được sửa hoặc thay bằng fallback JSON hợp lệ.

| Metric | V1 | V2 | Nhận xét |
|---|---:|---:|---|
| faithfulness | 0.9801 | 0.9426 | V1 cao hơn; cả hai đạt bonus ≥ 0.9 |
| answer_relevancy | 0.9139 | 0.8977 | V1 cao hơn |
| context_recall | 1.0000 | 1.0000 | Hòa |
| context_precision | 0.9450 | 0.9483 | V2 nhỉnh hơn |

V1 ngắn gọn nên ít phát sinh diễn giải ngoài context, phù hợp với faithfulness và answer relevancy cao hơn. V2 có cấu trúc chi tiết hơn và đạt context precision nhỉnh hơn, nhưng phần diễn giải bổ sung làm hai chỉ số còn lại giảm nhẹ. Cả hai phiên bản đều vượt mục tiêu faithfulness 0.8.

## URL LangSmith

- Project: https://smith.langchain.com/o/c0ce9528-832a-4c55-8553-b2abf6bff219/projects/p/3b582186-c006-497c-bd9e-5aedd8826d98
- Prompt V1: https://smith.langchain.com/prompts/truong-minh-hoang-day22-rag-v1/6a8857f5
- Prompt V2: https://smith.langchain.com/prompts/truong-minh-hoang-day22-rag-v2/b1ba609a

Các URL trên đã được kiểm tra trong tài khoản/organization đang đăng nhập. Project và hai prompt hiện ở chế độ private, vì vậy tiêu chí bonus “publicly accessible” chưa được tính là đã đạt.

## Danh sách tệp

- `01_langsmith_traces.png`: ảnh giao diện project với traces.
- `02_prompt_hub.png`: ảnh giao diện Prompt Hub với hai prompt.
- `02_ab_routing_log.txt`: log 50 câu A/B có nhãn V1/V2.
- `03_ragas_scores.png`: bảng điểm render trực tiếp từ report thật.
- `03_ragas_report.json`: bản sao báo cáo trong `data/`.
- `04_pii_demo_log.txt`: log 6 case PII.
- `04_json_demo_log.txt`: log 5 case JSON.

Ảnh RAGAS được tạo bởi `src/create_evidence.py` từ `data/ragas_report.json`; script không thay đổi các số đo.
