/** @odoo-module **/

console.log("🟢 [brand_selector.js] Script cargado correctamente");

setTimeout(() => {
    const imageButtons = document.querySelectorAll("[data-brand-id]");
    const selectBrand = document.querySelector("select[name='brand_id']");
    const selectModel = document.querySelector("select[name='model_id']");
    const selectYear = document.querySelector("select[name='year_id']");
    const selectVersion = document.querySelector("select[name='version_id']");

    const clearAndInit = (select, placeholder) => {
        if (select) select.innerHTML = `<option value="">${placeholder}</option>`;
    };

    const fetchData = async (url, payload) => {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
    
        const json = await response.json();
        if (!Array.isArray(json.result)) {
            console.error("❌ La propiedad `result` no es una lista:", json);
            return [];
        }
        return json.result;
    };

    const loadYearsByBrand = async (brandId) => {
        const years = await fetchData('/api/brand-years', { brand_id: brandId });
        clearAndInit(selectYear, "Selecciona un año");
        clearAndInit(selectModel, "Selecciona un modelo");
        clearAndInit(selectVersion, "Selecciona una versión");
        years.forEach(y => {
            const opt = new Option(y.name, y.id);
            selectYear.appendChild(opt);
        });
    };

    const loadModelsByBrandAndYear = async (brandId, yearId) => {
        const models = await fetchData('/api/models-by-brand-year', {
            brand_id: brandId,
            year_id: yearId
        });
        clearAndInit(selectModel, "Selecciona un modelo");
        clearAndInit(selectVersion, "Selecciona una versión");
        models.forEach(m => {
            const opt = new Option(m.name, m.id);
            selectModel.appendChild(opt);
        });
    };

    const loadVersions = async (modelId) => {
        const versions = await fetchData('/api/versions', { model_id: modelId });
        clearAndInit(selectVersion, "Selecciona una versión");
        versions.forEach(v => {
            const opt = new Option(v.name, v.id);
            selectVersion.appendChild(opt);
        });
    };

    if (selectBrand) {
        selectBrand.addEventListener("change", (e) => {
            const brandId = e.target.value;
            if (brandId) {
                loadYearsByBrand(brandId);
            }
        });
    }

    if (selectYear) {
        selectYear.addEventListener("change", (e) => {
            const yearId = e.target.value;
            const brandId = selectBrand.value;
            if (yearId && brandId) {
                loadModelsByBrandAndYear(brandId, yearId);
            }
        });
    }

    if (selectModel) {
        selectModel.addEventListener("change", (e) => {
            const modelId = e.target.value;
            if (modelId) {
                loadVersions(modelId);
            }
        });
    }

    imageButtons.forEach((img) => {
        img.addEventListener("click", () => {
            const brandId = img.dataset.brandId;
            if (brandId) {
                selectBrand.value = brandId;
                selectBrand.dispatchEvent(new Event("change"));
            }
        });
    });
}, 500);
