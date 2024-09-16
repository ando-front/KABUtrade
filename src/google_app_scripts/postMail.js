function doGet(e) {
  return ContentService.createTextOutput(
    "This app only accepts POST requests."
  );
}

function doPost(e) {
  // リクエストからシグナルのリストを取得
  const signals = JSON.parse(e.postData.contents).signals;
  let subject = "シグナル通知";
  let message = "";

  const footerMessage = `
  買いシグナル：日足が 75 日線を下から上に抜けて陽線で終わる、または陰線が 9 日間または 13 日間連続する。
  売りシグナル：日足が 75 日線を上から下に抜けて陰線で終わる、または陽線が 9 日間または 13 日間連続する。

  ゴールデンクロス（短期の移動平均線が長期の移動平均線を下から上に抜ける現象）が発生した場合は買いシグナル、
  デッドクロス（短期の移動平均線が長期の移動平均線を上から下に抜ける現象）が発生した場合は売りシグナルとします。

  パンパカパン(Buy_Signal_MA_PPP/Sell_Signal_MA_reverse_PPP):
   移動平均線が 5, 20, 60, 100, 200, 30 日の順番で高い場合は買いシグナル、逆に低い場合は売りシグナルとします。

  下半身(buy_signal_lower_harf/sell_signal_Reverse_lower_half)：
    買いシグナル 5 日線が上昇トレンドで、前日の日足線が 5 日線より下にあり、かつ、当日の日足線が陽線で 5 日線を実体の半分以上突き抜けていれば、買いシグナルとします。逆を逆下半身として売りシグナルとします。

  くちばし(buy_signal_bird_beak/sell_signal_reverse_bird_beak:):
    5 日線と 10 日線が上昇トレンドで、前日の 5 日線が 10 日線より下にあり、かつ、当日の 5 日線が 10 日線を上抜けていれば、買いシグナルとします。逆を売りシグナルとします。
  `;

  // 各シグナルに対してメッセージを作成
  signals.forEach((signal) => {
    const { symbol, signalType, signalKind } = signal;
    if (signalType === "Buy") {
      message += `賢二さん、${symbol}の買いシグナル（${signalKind}）が出ましたので、買い注文を入れてください。\n`;
    } else if (signalType === "Sell") {
      message += `賢二さん、${symbol}の売りシグナル（${signalKind}）が出ましたので、売り注文を入れてください。\n`;
    } else {
      message += `本日は${symbol}の買いor売りシグナルはありませんでした。\n`;
    }
  });

  // メール送信
  MailApp.sendEmail({
    to: "angie07.inet@gmail.com",
    subject: subject,
    body: message + "\n" + footerMessage,
  });

  // 正常終了のレスポンスを返す
  return ContentService.createTextOutput("Email sent.");
}
