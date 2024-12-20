def helper():
    return """『投資一點通』是一個幫助在投資的路上可以更順利的 AI！你可以詢問我股票或金融相關的問題，但是不相關的問題我可不吃喔！你可以問：
\t1. 告訴我公司名稱或股票的代號和時間區間（比如說過去五年），我將會繪製出股價的表現與 SPY 進行比較，並列出相關的指標（例如 Sharpe Ratio）！
\t2. 告訴我你想要配置資產的股票，我將會透過回測幫你找出適合的資產配置！
\t3. 詢問我與財金相關的問題！

祝您在投資的旅途上順利，隨便買都能發大財！"""

if __name__ == "__main__":
    print(helper())
