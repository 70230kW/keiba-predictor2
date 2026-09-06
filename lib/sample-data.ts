export type HorsePrediction = { gate:number; number:number; name:string; sexAge:string; jockey:string; weight:number; winProbability:number; top3Probability:number; fitness:number; courseFit:number; paceFit:number; note:string };
export const race = { venue:"東京", number:11, name:"秋風ステークス", condition:"3歳以上 オープン", course:"芝 1,800m・左", going:"良", startAt:"15:45", modelVersion:"baseline v0.1" };
export const predictions: HorsePrediction[] = [
  {gate:4,number:7,name:"アストラルリーフ",sexAge:"牡4",jockey:"高橋",weight:57,winProbability:24.8,top3Probability:58.4,fitness:91,courseFit:88,paceFit:84,note:"同距離で安定。終いの持続力が今回の展開に合う。"},
  {gate:2,number:3,name:"ブルーオービット",sexAge:"牝5",jockey:"佐々木",weight:55,winProbability:19.6,top3Probability:49.7,fitness:86,courseFit:92,paceFit:79,note:"東京芝への適性が高く、近3走の指数も上向き。"},
  {gate:6,number:11,name:"ノースウインド",sexAge:"牡3",jockey:"石川",weight:56,winProbability:15.1,top3Probability:43.2,fitness:89,courseFit:76,paceFit:90,note:"前傾ラップで浮上。斤量差もプラス材料。"},
  {gate:1,number:1,name:"ミッドナイトベル",sexAge:"牝4",jockey:"田辺",weight:55,winProbability:11.4,top3Probability:35.8,fitness:78,courseFit:85,paceFit:81,note:"内枠を活かせればロスなく運べる。"},
  {gate:5,number:9,name:"グランドパルス",sexAge:"牡5",jockey:"横山",weight:58,winProbability:9.2,top3Probability:30.1,fitness:82,courseFit:73,paceFit:75,note:"地力は上位。負担重量への対応が鍵。"}
];
