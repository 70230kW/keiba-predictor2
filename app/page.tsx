import { predictions, race } from "@/lib/sample-data";
const maxProbability=Math.max(...predictions.map((horse)=>horse.winProbability));

export default function Home(){
 return <main>
  <header className="topbar"><a className="brand" href="#top" aria-label="KEIBA LAB ホーム"><span className="brandMark">K</span><span>KEIBA LAB</span></a><div className="modelState"><span/>DEMO / 未学習</div></header>
  <section className="workspace" id="top">
   <div className="raceHeader"><div><p className="eyebrow">RACE ANALYSIS / 架空レース</p><h1>{race.venue} {race.number}R <span>{race.name}</span></h1><p className="raceMeta">{race.condition}　{race.course}　馬場：{race.going}</p></div><div className="startTime"><span>発走</span><strong>{race.startAt}</strong></div></div>
   <div className="principle"><span className="shield" aria-hidden="true">✓</span><div><strong>市場評価から独立した予測</strong><p>オッズ・人気・投票割合・予想印は、モデル入力に使用していません。</p></div><code>デモ表示・未学習</code></div>
   <div className="contentGrid">
    <section className="ranking" aria-labelledby="ranking-title">
     <div className="sectionTitle"><div><p>MODEL RANKING</p><h2 id="ranking-title">勝率ランキング</h2></div><span>上位5頭</span></div>
     <div className="horseList">{predictions.map((horse,index)=>
      <article className={`horseCard ${index===0?"leader":""}`} key={horse.number}>
       <div className="rank">{String(index+1).padStart(2,"0")}</div><div className={`horseNumber gate${horse.gate}`}>{horse.number}</div>
       <div className="horseIdentity"><h3>{horse.name}</h3><p>{horse.sexAge}　{horse.weight}kg　騎手 {horse.jockey}</p></div>
       <div className="probability"><div><span>推定勝率</span><strong>{horse.winProbability}<small>%</small></strong></div><div className="bar"><i style={{width:`${(horse.winProbability/maxProbability)*100}%`}}/></div></div>
       <div className="top3"><span>3着内</span><strong>{horse.top3Probability}%</strong></div>
      </article>)}</div>
    </section>
    <aside className="analysis" aria-labelledby="analysis-title">
     <div className="sectionTitle"><div><p>TOP PICK</p><h2 id="analysis-title">本命馬の分析</h2></div></div>
     <div className="pickHero"><div className="bigNumber">{predictions[0].number}</div><div><span>AI総合1位</span><h3>{predictions[0].name}</h3></div></div>
     <div className="scoreGrid"><Score label="近走能力" value={predictions[0].fitness}/><Score label="コース適性" value={predictions[0].courseFit}/><Score label="展開適性" value={predictions[0].paceFit}/></div>
     <div className="reason"><span>分析メモ</span><p>{predictions[0].note}</p></div>
     <dl className="dataPolicy"><div><dt>使用データ</dt><dd>戦績・タイム・条件・騎手・血統</dd></div><div><dt>除外データ</dt><dd>オッズ・人気・投票行動・予想印</dd></div></dl>
    </aside>
   </div>
   <details className="dataFoundation"><summary>実データの取り込み準備</summary><div className="details"><p>共通CSVを検査し、過去の戦績から学習用データを作成できます。データ提供元への接続とモデル学習は未実施です。</p><p>CSVはこの画面では送信・保存しません。取得元の利用条件を確認して、開発環境で取り込んでください。</p><a href="/templates/results.csv" download>CSVひな形をダウンロード</a></div></details>
   <p className="disclaimer">表示データは画面開発用のサンプルです。予測は的中や利益を保証するものではありません。</p>
  </section>
 </main>
}
function Score({label,value}:{label:string;value:number}){return <div className="score"><span>{label}</span><strong>{value}</strong><div><i style={{width:`${value}%`}}/></div></div>}
