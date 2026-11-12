"use strict";

const tools = document.querySelector("[data-filters]");
if (tools) {
  const search = document.querySelector("#project-search");
  const category = document.querySelector("#project-category");
  const cards = [...document.querySelectorAll("[data-project]")];
  const count = document.querySelector("[data-result-count]");
  const empty = document.querySelector("[data-empty]");
  const filter = () => {
    const query = search.value.trim().toLocaleLowerCase("de");
    let visible = 0;
    for (const card of cards) {
      const matches = card.dataset.search.toLocaleLowerCase("de").includes(query)
        && (!category.value || card.dataset.category === category.value);
      card.hidden = !matches;
      if (matches) visible += 1;
    }
    count.textContent = `${visible} von ${cards.length} Projekten`;
    empty.hidden = visible !== 0;
  };
  tools.hidden = false;
  search.addEventListener("input", filter);
  category.addEventListener("change", filter);
  filter();
}
