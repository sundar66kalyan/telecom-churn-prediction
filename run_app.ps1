Write-Host "🚀 Starting Telecom Churn Prediction System..." -ForegroundColor Cyan
Write-Host "="*50 -ForegroundColor Yellow

Write-Host "`n📦 Creating model files..." -ForegroundColor Green
python create_model_files.py

Write-Host "`n🚀 Launching Streamlit App..." -ForegroundColor Green
streamlit run app.py
