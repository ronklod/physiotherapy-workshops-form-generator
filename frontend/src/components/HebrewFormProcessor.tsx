import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './HebrewFormProcessor.css';
import ParticipantTable from './ParticipantTable';

interface Participant {
  name: string;
  id: string;
  receipt_number: string;
  amount: string;
}

interface ProcessTextResponse {
  activity_type: string | null;
  participants: Participant[];
  total_participants: number;
  success: boolean;
  message: string;
}

interface HealthResponse {
  status: string;
  groq_ai: string;
  capabilities: {
    ai_extraction: boolean;
    regex_fallback: boolean;
  };
}

const HebrewFormProcessor: React.FC = () => {
  const [inputText, setInputText] = useState('');
  const [activityType, setActivityType] = useState('');
  const [date, setDate] = useState('');
  const [processedData, setProcessedData] = useState<ProcessTextResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [aiStatus, setAiStatus] = useState<HealthResponse | null>(null);

  // Check AI status on component mount
  useEffect(() => {
    checkAiStatus();
  }, []);

  const checkAiStatus = async () => {
    try {
      const response = await axios.get('/api/health');
      setAiStatus(response.data);
    } catch (err) {
      console.error('Failed to check AI status:', err);
    }
  };

  const handleProcessText = async () => {
    if (!inputText.trim()) {
      setError('אנא הכנס טקסט לעיבוד');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/process-text', {
        text: inputText,
        activity_type: activityType || null,
        date: date || null
      });

      setProcessedData(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'שגיאה בעיבוד הטקסט');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateDocument = async () => {
    if (!inputText.trim()) {
      setError('אנא הכנס טקסט לעיבוד');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/generate-document', {
        text: inputText,
        activity_type: activityType || null,
        date: date || null
      }, {
        responseType: 'blob'
      });

      // Create blob link to download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      
      // Extract filename from response headers
      const contentDisposition = response.headers['content-disposition'];
      let filename = 'physiotherapy_form.docx';
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename=(.+)/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }
      
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'שגיאה ביצירת המסמך');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearText = () => {
    setInputText('');
    setActivityType('');
    setDate('');
    setProcessedData(null);
    setError(null);
  };



  return (
    <div className="hebrew-form-processor">
      <div className="processor-card">
        <h2 className="processor-title">עיבוד טקסט באמצעות בינה מלאכותית</h2>
        
        {/* AI Status Indicator */}
        <div className="ai-status">
          {aiStatus?.capabilities.ai_extraction ? (
            <div className="status-indicator ai-enabled">
              <span className="status-icon">🤖</span>
              <span>בינה מלאכותית פעילה - עיבוד חכם של טקסט טבעי</span>
            </div>
          ) : (
            <div className="status-indicator ai-disabled">
              <span className="status-icon">⚙️</span>
              <span>מצב רגיל - עיבוד טקסט מובנה בלבד</span>
            </div>
          )}
        </div>

        {/* Form Controls */}
        <div className="form-controls">
          <div className="control-row">
            <div className="control-group">
              <label htmlFor="activity-select" className="control-label">
                סוג פעילות:
              </label>
              <select
                id="activity-select"
                className="activity-select"
                value={activityType}
                onChange={(e) => setActivityType(e.target.value)}
                disabled={isLoading}
              >
                <option value="">בחר סוג פעילות...</option>
                <option value="לאחר לידה">לאחר לידה</option>
                <option value="הריון">הריון</option>
              </select>
            </div>

            <div className="control-group">
              <label htmlFor="date-input" className="control-label">
                תאריך:
              </label>
              <input
                id="date-input"
                type="text"
                className="date-input"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                placeholder="למשל: יוני 2024"
                disabled={isLoading}
              />
            </div>
          </div>
        </div>


        
        <div className="input-section">
          <label htmlFor="hebrew-input" className="input-label">
            הכנס את הטקסט כאן:
          </label>
          <textarea
            id="hebrew-input"
            className="hebrew-textarea"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder={aiStatus?.capabilities.ai_extraction 
              ? `בינה מלאכותית פעילה! ניתן להכניס טקסט טבעי בעברית.

דוגמה לטקסט טבעי:
"רחל כהן השתתפה בהתעמלות הריון. תעודת הזהות שלה 123456789, היא שילמה 250 שקלים וקיבלה קבלה מספר 12345."

או טקסט מובנה מסורתי:
שם: רחל כהן
תעודת זהות: 123456789
מספר קבלה: 12345
סכום ששולם: 250 ש״ח`
              : `התעמלות הריון - דצמבר 2023

שם: רחל כהן
תעודת זהות: 123456789
מספר קבלה: 12345
סכום ששולם: 250 ש״ח

שם: שרה לוי
תעודת זהות: 987654321
מספר קבלה: 67890
סכום ששולם: 300 ₪`}
            rows={12}
            disabled={isLoading}
          />
        </div>

        <div className="button-section">
          <button
            className="btn btn-primary"
            onClick={handleProcessText}
            disabled={isLoading || !inputText.trim()}
          >
            {isLoading ? 'מעבד...' : 'תצוגה מקדימה'}
          </button>
          
          <button
            className="btn btn-success"
            onClick={handleGenerateDocument}
            disabled={isLoading || !inputText.trim()}
          >
            {isLoading ? 'יוצר מסמך...' : 'צור מסמך Word'}
          </button>
          
          <button
            className="btn btn-secondary"
            onClick={handleClearText}
            disabled={isLoading}
          >
            נקה הכל
          </button>
        </div>

        {error && (
          <div className="error-message">
            <strong>שגיאה:</strong> {error}
          </div>
        )}

        {isLoading && (
          <div className="loading-section">
            <div className="loading-spinner"></div>
            <p>
              {aiStatus?.capabilities.ai_extraction 
                ? 'מעבד טקסט באמצעות בינה מלאכותית...' 
                : 'מעבד את הטקסט...'
              }
            </p>
          </div>
        )}

        {/* Document Title Preview */}
        {(activityType || date) && (
          <div className="title-preview">
            <h4>תצוגה מקדימה של כותרת המסמך:</h4>
            <div className="preview-title">
              {activityType && date ? `${activityType} - ${date}` : 
               activityType ? activityType : 
               date ? date : ''}
            </div>
          </div>
        )}

        {processedData && (
          <div className="results-section">
            <h3 className="results-title">תוצאות העיבוד</h3>
            <div className="results-summary">
              <p><strong>סוג פעילות:</strong> {processedData.activity_type || 'לא זוהה'}</p>
              <p><strong>מספר משתתפים:</strong> {processedData.total_participants}</p>
              <p className="processing-method">
                <strong>שיטת עיבוד:</strong> {
                  aiStatus?.capabilities.ai_extraction 
                    ? 'בינה מלאכותית (Groq AI)' 
                    : 'עיבוד רגיל'
                }
              </p>
            </div>
            
            {processedData.participants.length > 0 && (
              <ParticipantTable participants={processedData.participants} />
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default HebrewFormProcessor; 