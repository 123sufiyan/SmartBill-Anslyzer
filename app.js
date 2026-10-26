const defaults = { previous:12480, current:12892, unitRate:.31, offpeakRate:.18, standing:.52, days:30, peak:72, standby:42 };
const history = [
  { month:"2026-01", kwh:310, cost:108 },
  { month:"2026-02", kwh:295, cost:104 },
  { month:"2026-03", kwh:322, cost:112 },
  { month:"2026-04", kwh:318, cost:111 },
  { month:"2026-05", kwh:412, cost:137 },
];
const $ = (id) => document.getElementById(id);

function value(id){ return Number($(id).value); }
function money(n){ return `₹${n.toFixed(2)}`; }

function analyze(){
  const kwh = Math.max(0, value("current") - value("previous"));
  const peakKwh = kwh * value("peak") / 100;
  const offpeakKwh = kwh - peakKwh;
  const bill = peakKwh * value("unitRate") + offpeakKwh * value("offpeakRate") + value("standing") * value("days");
  const avg = history.slice(0,-1).reduce((s,m)=>s+m.kwh,0)/(history.length-1);
  const increase = ((history[history.length-1].kwh - avg)/avg)*100;
  const standbyKwh = value("standby") * 24 * value("days") / 1000;
  return { kwh, bill, costDay: bill/value("days"), increase, standbyKwh, standbyCost: standbyKwh*value("unitRate"), annual: bill/value("days")*365 };
}

function drawBars(canvas, labels, values, colors, markerIndex=-1){
  const ctx = canvas.getContext("2d");
  const ratio = window.devicePixelRatio || 1;
  const w = canvas.clientWidth || canvas.width, h = 320;
  canvas.width = w*ratio; canvas.height = h*ratio; ctx.scale(ratio, ratio); ctx.clearRect(0,0,w,h);
  const plot = {x:50,y:22,w:w-86,h:230}; const max = Math.max(...values, 1);
  ctx.strokeStyle="#d8e2ed"; ctx.beginPath(); ctx.moveTo(plot.x,plot.y); ctx.lineTo(plot.x,plot.y+plot.h); ctx.lineTo(plot.x+plot.w,plot.y+plot.h); ctx.stroke();
  labels.forEach((label,i)=>{ const bw=plot.w/labels.length-24; const x=plot.x+12+i*(plot.w/labels.length); const bh=values[i]/max*(plot.h-28); const y=plot.y+plot.h-bh; ctx.fillStyle=colors[i]; ctx.fillRect(x,y,bw,bh); ctx.fillStyle="#102033"; ctx.font="13px Inter, sans-serif"; ctx.fillText(label,x,plot.y+plot.h+24); ctx.fillText(values[i].toFixed(0),x,y-8); if(i===markerIndex){ctx.fillStyle="#d92d20";ctx.fillText("anomaly",x,y-25);} });
}

function render(){
  const result = analyze();
  $("peakLabel").textContent = `${value("peak")}%`;
  $("totalKwh").textContent = result.kwh.toFixed(0);
  $("billCost").textContent = money(result.bill);
  $("costDay").textContent = money(result.costDay);
  $("increase").textContent = `${result.increase.toFixed(2)}%`;
  $("standbyCost").textContent = money(result.standbyCost);
  $("annual").textContent = money(result.annual);
  $("anomaly").textContent = result.increase >= 20 ? "Anomaly: 2026-05" : "No anomaly";
  $("riskBadge").textContent = result.increase >= 20 ? "High increase" : "Stable";
  $("riskBadge").className = result.increase >= 20 ? "danger" : "ok";
  drawBars($("trendChart"), history.map(m=>m.month.slice(5)), history.map(m=>m.kwh), ["#1769d2","#1769d2","#1769d2","#1769d2","#d92d20"], 4);
  drawBars($("driverChart"), ["Peak", "Off-peak", "Standing", "Standby"], [result.kwh*value("peak")/100*value("unitRate"), result.kwh*(100-value("peak"))/100*value("offpeakRate"), value("standing")*value("days"), result.standbyCost], ["#d92d20","#1769d2","#c77700","#168a45"]);
  const rows = [
    ["Shift laundry and charging off-peak", "Medium", "Immediate"],
    ["Use smart plugs for standby loads", money(result.standbyCost), "1-3 months"],
    ["Check fridge/freezer seals and thermostat", "High if faulty", "1 month"],
    ["Replace inefficient lighting", "Low-medium", "3-6 months"],
  ];
  $("savingsRows").innerHTML = rows.map(r=>`<tr><td>${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td></tr>`).join("");
}

Object.keys(defaults).forEach(id => $(id).addEventListener("input", render));
$("reset").addEventListener("click", () => { Object.entries(defaults).forEach(([id,v]) => $(id).value = v); render(); });
window.addEventListener("resize", render);
render();
