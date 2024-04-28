function doGet(e) {
  return ContentService.createTextOutput(
    "This app only accepts POST requests."
  );
}

// この関数はHTTP POSTリクエストを受け取り、そのリクエストのパラメータに含まれる`signalType`に応じて、異なるメールを送信します。この関数をGASのウェブアプリケーションとしてデプロイし、得られたエンドポイントURLに対して適切な`signalType`パラメータ（`buy`または`sell`）を含むPOSTリクエストを送信することで、メールの自動送信が行われます。
function doPost(e) {
  // リクエストから信号の種類とシグナルの詳細を取得
  var signalType = e.parameter.signalType;
  var signalKind = e.parameter.signalKind;
  var subject = "";
  var message = "";
  var footerMessage =
    "買いシグナル：日足が 75 日線を下から上に抜けて陽線で終わる、または陰線が 9 日間または 13 日間連続する。\n売りシグナル：日足が 75 日線を上から下に抜けて陰線で終わる、または陽線が 9 日間または 13 日間連続する。\nBuy_Signal_MA_PPP/Sell_Signal_MA_reverse_PPP: 移動平均線が 5, 20, 60, 100, 200, 30 日の順番で高い場合は買いシグナル、逆に低い場合は売りシグナルとします。<br>ゴールデンクロス（短期の移動平均線が長期の移動平均線を下から上に抜ける現象）が発生した場合は買いシグナル、デッドクロス（短期の移動平均線が長期の移動平均線を上から下に抜ける現象）が発生した場合は売りシグナルとします。\n buy_signal_lower_harf/sell_signal_Reverse_lower_half:下半身：買いシグナルシグナル 5 日線が上昇トレンドで、前日の日足線が 5 日線より下にあり、かつ、当日の日足線が陽線で 5 日線を実体の半分以上突き抜けていれば、買いシグナルとします。逆を逆下半身として売りシグナルとします。\n </>buy_signal_bird_beak/sell_signal_reverse_bird_beak:くちばし:5 日線と 10 日線が上昇トレンドで、前日の 5 日線が 10 日線より下にあり、かつ、当日の 5 日線が 10 日線を上抜けていれば、買いシグナルとします。逆を売りシグナルとします。";

  // 信号の種類に応じて件名と本文を設定
  if (signalType === "Buy") {
    subject = "買いシグナルの通知";
    message =
      "賢二さん、SP500の買いシグナル（" +
      signalKind +
      "）が出ましたので、買い注文を入れてください。";
  } else if (signalType === "Sell") {
    subject = "売りシグナルの通知";
    message =
      "賢二さん、SP500の売りシグナル（" +
      signalKind +
      "）が出ましたので、売り注文を入れてください。";
  } else {
    // 不明な信号の種類の場合
    subject = "買いor売りシグナルはありませんでした";
    message = "本日は買いor売りシグナルはありませんでした";
  }

  // メール送信
  MailApp.sendEmail({
    to: "angie07.inet@gmail.com",
    subject: subject,
    body: message + "\n" + footerMessage,
  });

  // 正常終了のレスポンスを返す
  return ContentService.createTextOutput("Email sent.");
}
