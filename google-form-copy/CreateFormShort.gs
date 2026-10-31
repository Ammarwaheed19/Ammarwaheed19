function createForm() {
  var IMG = 'https://raw.githubusercontent.com/Ammarwaheed19/Ammarwaheed19/claude/friendly-brown-lfa77x/google-form-copy/';
  var form = FormApp.create('اکیڈمی ٹیسٹ');
  form.setIsQuiz(true);

  form.addTextItem().setTitle('نام').setRequired(true);
  form.addTextItem().setTitle('گروپ نمبر/ نام').setRequired(true);
  var sec = form.addMultipleChoiceItem().setTitle('سیکشن').setRequired(true);
  sec.setChoices([sec.createChoice('پلگ اینڈ پلے'), sec.createChoice('رومن')]);
  form.addSectionHeaderItem().setTitle('اکیڈمی ٹیسٹ').setHelpText('اللہ کو حاضرو ناظر جانتے ہوئے ٹیسٹ دیں');

  // [question, options, correct option number (1-3), picture]
  var Q = [
    ['آخری حرف پر "ینَ" مطلب ؟', ['والے', 'جس نے', 'دونوں'], 1],
    ['المُکذِّبِینَ....ترجمہ ؟', ['دو جھٹلانے والے', 'سب جھٹلانے والے', 'سب جھوٹ کہنے والے'], 2],
    ['السائِحُونَ.....ترجمہ؟', ['روزہ رکھنے والے', 'دو روزے دار', 'انہوں نے روزہ رکھا'], 1],
    ['اس کے شروع میں "اصحاب" لگا کر ترجمہ کریں', ['بائیں ہاتھ والے', 'دائیں ہاتھ والے', 'دو ہاتھ والے'], 1, 'img_mashama.png'],
    ['عشرہ= 10  اگر " 14" بنانا ہو تو کس کو کس سے جوڑینگے ؟', ['اربعین+ عشر', 'اربعة + عشر', 'ثلاثة + عشر'], 2],
    ['صحیح ترجمہ کیا ہوگا؟', ['90---نوے', '19---انیس', '29----انتیس'], 1, 'img_tisa.png'],
    ["ترپن 53 ' عربی میں کیسے لکھیں گے؟ '", ['ثلاثة و خمسینَ', 'خمسینَ و اربع', 'خمسہ وثلاثین'], 1],
    ['"یوم الخمیس"... کون سا دن ہے', ['بدھ', 'جمعرات', 'ہفتہ'], 2],
    ['ترجمہ؟', ['بہت ہی رحیم', 'رحم کرنے والا', 'رحمت والا'], 3, 'img_rahma.png'],
    ['جمع کے لیے کیا استعمال ہوگا', ['ذو', 'ذی', 'اولو'], 3]
  ];

  Q.forEach(function (q) {
    if (q[3]) form.addImageItem().setImage(UrlFetchApp.fetch(IMG + q[3]).getBlob());
    var item = form.addMultipleChoiceItem().setTitle(q[0]).setRequired(true).setPoints(2);
    item.setChoices(q[1].map(function (opt, i) { return item.createChoice(opt, i + 1 === q[2]); }));
  });

  Logger.log('EDIT LINK: ' + form.getEditUrl());
  Logger.log('STUDENT LINK: ' + form.getPublishedUrl());
}
