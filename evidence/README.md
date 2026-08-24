# Minh chứng Day 22 — LangSmith + Prompt Versioning

## Kết quả đã đo

- Bước 1: 50/50 câu hỏi chạy qua RAG pipeline; knowledge base được chia thành 107 chunks và index bằng FAISS.
- Bước 2: hai prompt `truong-minh-hoang-day22-rag-v1` và `truong-minh-hoang-day22-rag-v2` đã được push rồi pull lại từ Prompt Hub. A/B routing tất định phân bổ V1=19, V2=31 trên 50 request ID.
- Bước 3: chạy đủ 50 QA qua cả V1 và V2. API LangSmith xác nhận project có ít nhất 100 root traces; giao diện Stats tại thời điểm chụp hiển thị `Trace Count = 323`.
- Bước 4: 6 case PII và 5 case JSON đều qua assertion; PII được che và JSON lỗi được sửa hoặc thay bằng fallback JSON hợp lệ.
- Chạy tổng: `python src/run_all.py` đã chạy liên tiếp cả 4 bước trong một tiến trình và kết thúc với 4/4 trạng thái `PASS`; log đầy đủ được lưu tại `05_run_all_log.txt`.

| Metric | V1 | V2 | Nhận xét |
|---|---:|---:|---|
| faithfulness | 0.9612 | 0.9504 | V1 cao hơn; cả hai đạt bonus ≥ 0.9 |
| answer_relevancy | 0.9128 | 0.9056 | V1 cao hơn |
| context_recall | 1.0000 | 1.0000 | Hòa |
| context_precision | 0.9383 | 0.9417 | V2 nhỉnh hơn |

V1 ngắn gọn nên ít phát sinh diễn giải ngoài context, phù hợp với faithfulness và answer relevancy cao hơn. V2 có cấu trúc chi tiết hơn và đạt context precision nhỉnh hơn, nhưng phần diễn giải bổ sung làm hai chỉ số còn lại giảm nhẹ. Cả hai phiên bản đều vượt mục tiêu faithfulness 0.8.

## URL LangSmith

- Project: https://smith.langchain.com/o/c0ce9528-832a-4c55-8553-b2abf6bff219/projects/p/3b582186-c006-497c-bd9e-5aedd8826d98
- Public trace (không cần đăng nhập): https://smith.langchain.com/public/586a9099-c4f0-4533-a7c6-666d0dc65a17/r/01a03339-7e32-7881-9a98-55380762e3f9?start_time=2026-08-24T10%3A03%3A21.010911Z
- Prompt V1: https://smith.langchain.com/prompts/truong-minh-hoang-day22-rag-v1/6a8857f5
- Prompt V2: https://smith.langchain.com/prompts/truong-minh-hoang-day22-rag-v2/b1ba609a

LangSmith hiện không cung cấp tùy chọn public cho toàn bộ tracing project. Vì vậy bài nộp giữ URL project để chứng minh tổng số traces và bổ sung một root trace đã được share công khai. Public trace đã được kiểm tra HTTP 200 mà không gửi thông tin đăng nhập; người chấm có thể xem question, retrieved context và answer qua URL này. Hai prompt trên Prompt Hub vẫn ở chế độ private.

## Danh sách tệp

- `01_langsmith_traces.png`: ảnh giao diện project với traces.
- `02_prompt_hub.png`: ảnh giao diện Prompt Hub với hai prompt.
- `02_ab_routing_log.txt`: log 50 câu A/B có nhãn V1/V2.
- `03_ragas_scores.png`: bảng điểm render trực tiếp từ report thật.
- `03_ragas_report.json`: bản sao báo cáo trong `data/`.
- `04_pii_demo_log.txt`: log 6 case PII.
- `04_json_demo_log.txt`: log 5 case JSON.
- `05_run_all_log.txt`: log một lần chạy xuyên suốt Bước 1 → Bước 4, có bảng tổng kết 4/4 `PASS`.

Ảnh RAGAS được tạo bởi `src/create_evidence.py` từ `data/ragas_report.json`; script không thay đổi các số đo.
