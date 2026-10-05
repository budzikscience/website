// Mobile menu
const btn = document.querySelector('.menu-btn'), menu = document.getElementById('menu');
btn.addEventListener('click', () => {
  const open = menu.classList.toggle('open');
  btn.setAttribute('aria-expanded', open);
});
menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
  menu.classList.remove('open'); btn.setAttribute('aria-expanded', false);
}));

// Nav border on scroll
const nav = document.querySelector('.nav');
addEventListener('scroll', () => nav.classList.toggle('scrolled', scrollY > 8), { passive: true });

// Reveal on scroll
const io = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
}), { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// Play videos only when visible (saves battery/bandwidth)
const vio = new IntersectionObserver(es => es.forEach(e => {
  const v = e.target;
  if (e.isIntersecting) { v.play().catch(() => {}); } else { v.pause(); }
}), { threshold: 0.2 });
document.querySelectorAll('video').forEach(v => vio.observe(v));

// Publication search + year filter
const q = document.getElementById('pubq'), list = document.getElementById('publist');
if (q && list) {
  let year = 'all';
  const items = [...list.children], empty = document.getElementById('pubempty');
  const apply = () => {
    const t = q.value.trim().toLowerCase(); let n = 0;
    items.forEach(li => {
      const y = +li.dataset.year;
      const okY = year === 'all' || (year === 'old' ? y < 2017 : y === +year);
      const ok = okY && (!t || li.dataset.q.includes(t));
      li.hidden = !ok; if (ok) n++;
    });
    empty.hidden = n > 0;
  };
  q.addEventListener('input', apply);
  document.querySelectorAll('.chip').forEach(c => c.addEventListener('click', () => {
    document.querySelectorAll('.chip').forEach(x => x.classList.remove('on'));
    c.classList.add('on'); year = c.dataset.y; apply();
  }));
}
