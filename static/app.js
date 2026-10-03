document.addEventListener('click', async (e) => {
  if (e.target.matches('.check')) {
    const parent = e.target.closest('.exercise')
    const index = parseInt(parent.dataset.index, 10)
    const type = parent.dataset.type || 'short'
    let answer = ''
    if (type === 'mcq') {
      const sel = parent.querySelector('input[type=radio]:checked')
      answer = sel ? sel.value : ''
    } else {
      const input = parent.querySelector('.answer')
      answer = input ? input.value : ''
    }
    const gid = window.location.pathname.split('/').pop()
    const res = await fetch('/api/check', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({gid, qindex: index, answer})
    })
    const j = await res.json()
    const resultDiv = parent.querySelector('.result')
    if (j.ok) {
      resultDiv.textContent = j.correct ? 'Correcto ✅ ' + (j.feedback||'') : 'Incorrecto ❌ ' + (j.feedback||'')
    } else {
      resultDiv.textContent = 'Error: ' + (j.error||'')
    }
  }
})

// Optional: handle regenerate responses if triggered elsewhere
async function regenerateGrammar(gid) {
  const res = await fetch('/api/regenerate/' + gid, {method: 'POST'})
  return res.json()
}
