# ClinicSim AI API Contract v1.0

This document defines the API endpoints for the ClinicSim AI backend service. The purpose of this contract is to ensure that the frontend (Streamlit UI) and backend (Mock Server / Lemonade Server) can be developed independently and integrate seamlessly.

---

### Endpoint: `/ask_patient`

- **Method:** `POST`
- **Description:** Sends the current conversation history to the AI patient and gets the next response.
- **Request Body (JSON):**
  ```json
  {
    "history": [
      {"role": "user", "content": "您好，請問您哪裡不舒服？"},
      {"role": "assistant", "content": "醫生，我胸口很痛..."}
    ],
    "case_id": "chest_pain_01"
  }
  ```
- **Response Body (JSON):**
  ```json
  {
    "reply": "痛了一個小時了..."
  }
  ```

---

### Endpoint: `/get_feedback_report`

- **Method:** `POST`
- **Description:** Sends the entire conversation log to the AI analyst and gets a feedback report.
- **Request Body (JSON):**
  ```json
  {
    "full_conversation": [
      {"role": "user", "content": "您好，請問您哪裡不舒服？"},
      {"role": "assistant", "content": "醫生，我胸口很痛..."},
      {"role": "user", "content": "這種痛是像被石頭壓著，還是像針刺？"},
      {"role": "assistant", "content": "比較像是被大石頭壓住，喘不過氣..."}
    ],
    "case_id": "chest_pain_01"
  }
  ```
- **Response Body (JSON):**
  ```json
  {
    "report_text": "### 診後分析報告\n\n**問診要點分析：**\n- ✅ 發作時間 (Onset)\n- ❌ 誘發與緩解因子 (Provocation/Palliation)\n- ✅ 疼痛性質 (Quality)\n\n**總結：**\n本次問診..."
  }
  ```