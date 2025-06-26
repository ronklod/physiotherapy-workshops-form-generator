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
  grok_ai: string;
  capabilities: {
    ai_extraction: boolean;
    regex_fallback: boolean;
  };
}

const HebrewFormProcessor: React.FC = () => {
  const [inputText, setInputText] = useState('');
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
      const response = await axios.get('/health');
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
      const response = await axios.post('/process-text', {
        text: inputText
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
      const response = await axios.post('/generate-document', {
        text: inputText
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
    setProcessedData(null);
    setError(null);
  };

  const loadExampleText = (type: 'natural' | 'structured') => {
    if (type === 'natural') {
      setInputText(`התעמלות הריון - יוני 2024

שרה כהן השתתפה בקורס התעמלות הריון במהלך החודש. תעודת הזהות של שרה היא 123456789. היא שילמה 280 שקלים עבור הקורס וקיבלה קבלה מספר 12345.

גם רחל לוי הגיעה לקורסים. המספר זהות שלה 987654321, והיא שילמה 300 ש״ח. הקבלה שלה מספר 67890.

בנוסף, מיכל דוד (ת.ז 456789123) השתתפה גם היא. היא שילמה סכום של 250 שקלים וקבלה חשבונית 11111.`);
    } else {
      setInputText(`התעמלות לאחר לידה - יוני 2024

שם: ליאת ישראלי
תעודת זהות: 321654987
מספר קבלה: 98765
סכום ששולם: 200 ש״ח

שם: נועה גולדברג
תעודת זהות: 147258369
מספר קבלה: 55555
סכום ששולם: 225 ₪`);
    }
  };

  return (
    <div className="hebrew-form-processor">
      <div className="processor-card">
        <h2 className="processor-title">עיבוד טקסט עברי באמצעות בינה מלאכותית</h2>
        
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

        {/* Example Buttons */}
        <div className="example-section">
          <h3 className="example-title">דוגמאות:</h3>
          <div className="example-buttons">
            <button
              className="btn btn-example"
              onClick={() => loadExampleText('natural')}
              disabled={isLoading}
            >
              טקסט טבעי (עבור AI)
            </button>
            <button
              className="btn btn-example"
              onClick={() => loadExampleText('structured')}
              disabled={isLoading}
            >
              טקסט מובנה
            </button>
          </div>
        </div>
        
        <div className="input-section">
          <label htmlFor="hebrew-input" className="input-label">
            הכנס את הטקסט העברי כאן:
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
            {isLoading ? 'מעבד...' : 'עבד טקסט'}
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
            נקה
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

        {processedData && (
          <div className="results-section">
            <h3 className="results-title">תוצאות העיבוד</h3>
            <div className="results-summary">
              <p><strong>סוג פעילות:</strong> {processedData.activity_type || 'לא זוהה'}</p>
              <p><strong>מספר משתתפים:</strong> {processedData.total_participants}</p>
              <p className="processing-method">
                <strong>שיטת עיבוד:</strong> {
                  aiStatus?.capabilities.ai_extraction 
                    ? 'בינה מלאכותית (Grok AI)' 
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