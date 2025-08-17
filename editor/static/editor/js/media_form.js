// editor/static/editor/js/media_form.js

(function () {
  const $ = (q, c = document) => c.querySelector(q);
  const $$ = (q, c = document) => Array.from(c.querySelectorAll(q));

  document.addEventListener('DOMContentLoaded', () => {
    // ===== Description char counter =====
    const desc = $('#id_description');
    const counter = $('#desc-counter');
    if (desc && counter) {
      const update = () => counter.textContent = (desc.value || '').length;
      desc.addEventListener('input', update);
      update();
    }

    // ===== Type-dependent fields (Series only) =====
    const typeSelect = $('#id_type');
    const seriesFields = $$('.type-series-only');
    const toggleSeries = () => {
      const name = (typeSelect?.selectedOptions?.[0]?.text || '').toLowerCase();
      const isSeries = name === 'series' || name === 'сериал';
      seriesFields.forEach(el => el.style.display = isSeries ? '' : 'none');
      if (!isSeries) {
        const s = $('#id_number_of_seasons'); const e = $('#id_number_of_series');
        if (s) s.value = '';
        if (e) e.value = '';
      }
    };
    if (typeSelect) { typeSelect.addEventListener('change', toggleSeries); toggleSeries(); }

    // ===== Dates guard: end >= start =====
    const start = $('#id_start_year');
    const end = $('#id_end_year');
    const syncDates = () => {
      if (start && end && start.value) end.min = start.value;
      else if (end) end.removeAttribute('min');
    };
    if (start) start.addEventListener('change', syncDates);
    if (end) end.addEventListener('change', syncDates);
    syncDates();

    // ===== Genres filter (checkbox list) =====
    const genreFilter = $('#genre-filter');
    if (genreFilter) {
      genreFilter.addEventListener('input', () => {
        const q = genreFilter.value.trim().toLowerCase();
        $$('.checkbox-select-multiple label').forEach(label => {
          const txt = (label.textContent || '').toLowerCase();
          label.style.display = (!q || txt.includes(q)) ? '' : 'none';
        });
      });
    }

    // ===== Studios filter + chips (multi-select) =====
    const studioFilter = $('#studio-filter');
    const studiosSelect = $('#id_studios');
    const chipsBox = $('#studio-chips');

    const rebuildChips = () => {
      if (!studiosSelect || !chipsBox) return;
      chipsBox.innerHTML = '';
      Array.from(studiosSelect.options).forEach(opt => {
        if (!opt.selected) return;
        const chip = document.createElement('span');
        chip.className = 'chip';
        chip.textContent = opt.text;
        const x = document.createElement('button');
        x.type = 'button';
        x.className = 'chip-x';
        x.setAttribute('aria-label', 'Удалить');
        x.textContent = '×';
        x.addEventListener('click', () => { opt.selected = false; rebuildChips(); });
        chip.appendChild(x);
        chipsBox.appendChild(chip);
      });
    };

    if (studiosSelect) {
      if (!studiosSelect.size || studiosSelect.size < 8) studiosSelect.size = 8;
      studiosSelect.addEventListener('change', rebuildChips);
      rebuildChips();
    }
    if (studioFilter && studiosSelect) {
      const original = Array.from(studiosSelect.options).map(o => ({ v: o.value, t: o.text }));
      studioFilter.addEventListener('keydown', (e) => {
        // Быстрый выбор по Enter: если единственное совпадение — выбрать его.
        if (e.key === 'Enter') {
          e.preventDefault();
          const q = studioFilter.value.trim().toLowerCase();
          if (!q) return;
          const match = original.find(o => o.t.toLowerCase() === q) ||
                        original.find(o => o.t.toLowerCase().includes(q));
          if (match) {
            const opt = Array.from(studiosSelect.options).find(o => o.value === match.v);
            if (opt) { opt.selected = true; rebuildChips(); }
            studioFilter.value = '';
          }
        }
      });
      studioFilter.addEventListener('input', () => {
        const q = studioFilter.value.trim().toLowerCase();
        // запоминаем текущие выбранные
        const sel = new Set(Array.from(studiosSelect.selectedOptions).map(o => o.value));
        studiosSelect.innerHTML = '';
        original.forEach(({ v, t }) => {
          if (!q || t.toLowerCase().includes(q)) {
            const opt = document.createElement('option');
            opt.value = v; opt.text = t; opt.selected = sel.has(v);
            studiosSelect.appendChild(opt);
          }
        });
      });
    }

    // ===== Cover: drag & drop + preview + accept only jpg =====
    const drop = $('#cover-drop');
    const input = $('#id_cover');
    const preview = $('#cover-preview');
    if (input) input.setAttribute('accept', 'image/jpeg,.jpg');

    const showPreview = file => {
      if (!file) return;
      if (!/\.jpe?g$/i.test(file.name)) {
        notification('Допустимы только JPG файлы.', 'error');
        input.value = '';
        if (preview) preview.style.display = 'none';
        return;
      }
      const reader = new FileReader();
      reader.onload = e => {
        if (preview) { preview.src = e.target.result; preview.style.display = 'block'; }
      };
      reader.readAsDataURL(file);
    };

    if (input) input.addEventListener('change', () => showPreview(input.files?.[0]));
    if (drop && input) {
      const stop = e => { e.preventDefault(); e.stopPropagation(); };
      ['dragenter','dragover','dragleave','drop'].forEach(evt => drop.addEventListener(evt, stop, false));
      drop.addEventListener('drop', e => {
        const file = e.dataTransfer.files?.[0];
        if (file) {
          const dt = new DataTransfer();
          dt.items.add(file);
          input.files = dt.files;
          showPreview(file);
        }
      });
      drop.addEventListener('click', () => input.click());
    }
  });
})();
