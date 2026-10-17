// Raffle Math engine - draw odds and ticket cost arithmetic.
// Mirrored by oracle.py; keep the op order identical.

function _int(x, lo, msg) {
  if (!isFinite(x) || x % 1 !== 0 || x < lo) throw new Error(msg);
  return x;
}

function _check(tickets, total, prizes) {
  _int(total, 1, "tickets sold must be a whole number, 1 or more");
  if (total > 10000) throw new Error("keep tickets sold at 10000 or fewer");
  _int(prizes, 1, "prizes must be a whole number, 1 or more");
  if (prizes > 100) throw new Error("keep prizes at 100 or fewer");
  if (prizes > total) throw new Error("there cannot be more prizes than tickets sold");
  if (tickets !== null) {
    _int(tickets, 1, "your tickets must be a whole number, 1 or more");
    if (tickets > total) throw new Error("you cannot hold more tickets than were sold");
  }
}

function _s(n, one, many) {
  return n === 1 ? one : many;
}

// Chance that none of your tickets is drawn. Each ticket wins at most one prize.
function _noWin(k, n, p) {
  if (k + p > n) return 0;
  var r = 1;
  for (var i = 0; i < p; i++) r = r * ((n - k - i) / (n - i));
  return r;
}

function _tenths(t) {
  return Math.floor(t / 10) + "." + (t % 10) + "%";
}

function _p2(n) {
  return (n < 10 ? "0" : "") + n;
}

function _money(c) {
  return "$" + Math.floor(c / 100) + "." + _p2(c % 100);
}

// The odds truth: chance of at least one win.
function oddsTruth(tickets, total, prizes) {
  _check(tickets, total, prizes);
  var win = Math.floor((1 - _noWin(tickets, total, prizes)) * 1000 + 0.5);
  return tickets + " of " + total + " tickets with " + prizes + " " + _s(prizes, "prize", "prizes") +
    ": a " + _tenths(win) + " chance of at least one win, " + _tenths(1000 - win) + " of none.";
}

// The value truth: owner-entered price and prize value against the average payout.
function valueTruth(priceDollars, tickets, total, prizes, prizeDollars) {
  _check(tickets, total, prizes);
  if (!isFinite(priceDollars) || priceDollars < 0) throw new Error("ticket price must be 0 or more");
  if (!isFinite(prizeDollars) || prizeDollars < 0) throw new Error("prize value must be 0 or more");
  var price = Math.floor(priceDollars * 100 + 0.5);
  var prize = Math.floor(prizeDollars * 100 + 0.5);
  var cost = tickets * price;
  var ev = Math.floor((prizes * prize * tickets) / total + 0.5);
  var each = Math.floor((prizes * prize) / total + 0.5);
  var diff = ev - cost;
  var net = diff > 0 ? "ahead by " + _money(diff) : diff < 0 ? "behind by " + _money(-diff) : "even";
  return tickets + " " + _s(tickets, "ticket", "tickets") + " at " + _money(price) + " cost " + _money(cost) +
    ". Average prize value is " + _money(ev) + " (" + prizes + " " + _s(prizes, "prize", "prizes") + " of " +
    _money(prize) + " over " + total + " tickets, " + _money(each) + " per ticket). On average: " + net + ".";
}

// The target truth: fewest tickets that reach a chance you name.
function targetTruth(total, prizes, targetPct) {
  _check(null, total, prizes);
  if (!isFinite(targetPct) || targetPct <= 0 || targetPct > 100) throw new Error("target must be over 0 and at most 100 percent");
  var goal = targetPct / 100;
  for (var k = 1; k <= total; k++) {
    var w = 1 - _noWin(k, total, prizes);
    if (w >= goal) {
      return "To reach a " + targetPct + "% chance with " + prizes + " " + _s(prizes, "prize", "prizes") + " among " + total +
        " tickets, you would hold " + k + " " + _s(k, "ticket", "tickets") + " (" + _tenths(Math.floor(w * 1000 + 0.5)) + ").";
    }
  }
  throw new Error("no ticket count reaches that target");
}
