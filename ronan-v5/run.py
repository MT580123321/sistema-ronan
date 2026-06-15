from app import app

if __name__ == '__main__':
    print("\n🔥 Churrascaria do Ronan — Sistema Web")
    print("   Acesse: http://localhost:5000")
    print("   Login: admin / 123\n")
    app.run(debug=True, port=5000)
