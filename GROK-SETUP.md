# 🤖 Grok AI Integration Setup Guide

This guide will help you set up Grok AI integration for intelligent Hebrew text processing. With Grok AI, the system can understand natural Hebrew text and extract participant information much more accurately.

## 🆚 Without vs With Grok AI

### Without Grok AI (Regex Only)
**Input Format Required:**
```hebrew
שם: רחל כהן
תעודת זהות: 123456789
מספר קבלה: 12345
סכום ששולם: 250 ש״ח
```

### With Grok AI (Natural Language)
**Input Format Supported:**
```hebrew
רחל כהן השתתפה בהתעמלות הריון החודש. תעודת הזהות שלה 123456789, היא שילמה 250 שקלים וקיבלה קבלה מספר 12345.
```

## 🚀 Getting Started

### Step 1: Get Your Grok API Key

1. **Visit the Grok Console**: Go to [https://console.x.ai/](https://console.x.ai/)
2. **Sign Up/Login**: Create an account or log in if you already have one
3. **Navigate to API Keys**: Find the API section in your dashboard
4. **Create New Key**: Generate a new API key for your application
5. **Copy the Key**: Save your API key securely (you'll need it in the next step)

### Step 2: Set Environment Variable

Choose one of the following methods:

#### Option A: Export Command (Temporary)
```bash
export GROK_API_KEY="your-grok-api-key-here"
```

#### Option B: Add to ~/.bashrc or ~/.zshrc (Permanent)
```bash
echo 'export GROK_API_KEY="your-grok-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

#### Option C: Create .env file in backend directory
```bash
cd backend
echo "GROK_API_KEY=your-grok-api-key-here" > .env
```

### Step 3: Restart the Backend

After setting the API key, restart your backend server:

```bash
./start-backend.sh
```

### Step 4: Verify Integration

1. **Check API Status**: Visit [http://localhost:8000](http://localhost:8000)
2. **Look for**: `"grok_ai_integration": "enabled"`
3. **Health Check**: Visit [http://localhost:8000/health](http://localhost:8000/health)

## ✅ Testing the Integration

### Test Natural Hebrew Text

Try this example in the web interface:

```hebrew
התעמלות הריון - יוני 2024

שרה כהן השתתפה בקורס התעמלות הריון במהלך החודש. תעודת הזהות של שרה היא 123456789. היא שילמה 280 שקלים עבור הקורס וקיבלה קבלה מספר 12345.

גם רחל לוי הגיעה לקורסים. המספר זהות שלה 987654321, והיא שילמה 300 ש״ח. הקבלה שלה מספר 67890.

בנוסף, מיכל דוד (ת.ז 456789123) השתתפה גם היא. היא שילמה סכום של 250 שקלים וקבלה חשבונית 11111.
```

### Expected Results

The AI should extract:
- **3 participants** with complete information
- **Activity type**: התעמלות הריון
- **All names, IDs, receipt numbers, and amounts** correctly identified

## 🔧 Troubleshooting

### Common Issues

1. **"grok_ai_integration": "disabled"**
   - Check if your API key is set correctly
   - Restart the backend server
   - Verify the environment variable: `echo $GROK_API_KEY`

2. **API Request Failures**
   - Verify your API key is valid
   - Check your internet connection
   - Check API rate limits

3. **Extraction Not Working**
   - The system automatically falls back to regex if AI fails
   - Check backend logs for error messages
   - Try with different text formats

### Debug Commands

```bash
# Check if environment variable is set
echo $GROK_API_KEY

# Check backend health
curl http://localhost:8000/health

# Check setup help
curl http://localhost:8000/setup-help

# View backend logs
tail -f backend/logs/app.log  # if logging to file
```

## 📊 Performance Comparison

| Feature | Without Grok AI | With Grok AI |
|---------|----------------|---------------|
| **Text Format** | Structured only | Natural + Structured |
| **Accuracy** | Good for structured | Excellent for both |
| **Hebrew Support** | Basic | Advanced |
| **Context Understanding** | Limited | High |
| **Flexibility** | Low | High |

## 💡 Tips for Best Results

### Writing Natural Hebrew Text
- **Use full sentences**: "רחל כהן השתתפה בקורס"
- **Include context**: "תעודת הזהות של רחל היא..."
- **Natural flow**: Write as you would normally speak
- **Multiple formats**: Mix different ways of expressing the same information

### Sample Variations That Work
```hebrew
# Variation 1
שרה שילמה 250 שקלים, תעודת זהות 123456789, קבלה 12345

# Variation 2  
משתתפת: רחל לוי (ת.ז: 987654321) - תשלום: 300₪, מס' קבלה 67890

# Variation 3
מיכל דוד השתתפה בקורס. המספר זהות שלה: 456789123. היא שילמה 275 ש״ח וקיבלה חשבונית מספר 11111.
```

## 🔒 Security Notes

- **Never commit** your API key to version control
- **Use environment variables** for production
- **Rotate keys regularly** for security
- **Monitor usage** to prevent unexpected charges

## 📞 Support

If you encounter issues:

1. **Check Backend Logs**: Look for error messages in the terminal
2. **Test API Directly**: Use the Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs)
3. **Verify Setup**: Use [http://localhost:8000/setup-help](http://localhost:8000/setup-help)
4. **Check Grok Status**: Visit the [Grok Console](https://console.x.ai/) for API status

## 🎯 Next Steps

Once Grok AI is working:

1. **Try different text formats** to see the AI's flexibility
2. **Test with real workshop data** from your physiotherapy sessions  
3. **Experiment with mixed Hebrew/English text**
4. **Use the example buttons** in the web interface for quick testing

---

**Ready to experience intelligent Hebrew text processing? Set up your Grok API key and see the difference! 🚀** 