/** @odoo-module **/

console.log("🟢 [brand_selector.js] Script cargado correctamente");

setTimeout(() => {
    const imageButtons = document.querySelectorAll("[data-brand-id]");
    const selectBrand = document.querySelector("select[name='brand_id']");
    const selectModel = document.querySelector("select[name='model_id']");
    const selectYear = document.querySelector("select[name='year_id']");
    const selectVersion = document.querySelector("select[name='version_id']");

    const clearAndInit = (select, placeholder) => {
        if (select) {
            console.log(`🧹 Limpiando <select> y añadiendo placeholder: ${placeholder}`);
            select.innerHTML = `<option value="">${placeholder}</option>`;
        }
    };

    const fetchData = async (url, payload) => {
        console.log(`🔄 Enviando POST a ${url} con payload:`, payload);
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        const json = await response.json();
        console.log(`✅ Respuesta de ${url}:`, json);
        return Array.isArray(json.result) ? json.result : [];
    };

    const loadYearsByBrand = async (brandId) => {
        console.log(`📅 Cargando años para brand_id=${brandId}`);
        const years = await fetchData('/api/brand-years', { brand_id: brandId });
        clearAndInit(selectYear, "Selecciona un año");
        clearAndInit(selectModel, "Selecciona un modelo");
        clearAndInit(selectVersion, "Selecciona una versión");
        years.forEach(y => {
            console.log(`➕ Año añadido: ${y.name} (id=${y.id})`);
            const opt = new Option(y.name, y.id);
            selectYear.appendChild(opt);
        });
    };

    const loadModelsByBrandAndYear = async (brandId, yearId) => {
        console.log(`🚗 Cargando modelos para brand_id=${brandId}, year_id=${yearId}`);
        const models = await fetchData('/api/models-by-brand-year', {
            brand_id: brandId,
            year_id: yearId
        });
        clearAndInit(selectModel, "Selecciona un modelo");
        clearAndInit(selectVersion, "Selecciona una versión");
        models.forEach(m => {
            console.log(`➕ Modelo añadido: ${m.name} (id=${m.id})`);
            const opt = new Option(m.name, m.id);
            selectModel.appendChild(opt);
        });
    };

    const loadVersions = async (modelId, yearId) => {
        console.log(`🧩 Cargando versiones para model_id=${modelId}, year_id=${yearId}`);
        const versions = await fetchData('/api/versions', {
            model_id: modelId,
            year_id: yearId
        });
        clearAndInit(selectVersion, "Selecciona una versión");
        versions.forEach(v => {
            console.log(`➕ Versión añadida: ${v.name} (id=${v.id})`);
            const opt = new Option(v.name, v.id);
            selectVersion.appendChild(opt);
        });
    };

    if (selectBrand) {
        selectBrand.addEventListener("change", (e) => {
            const brandId = e.target.value;
            console.log(`📌 Cambio en selectBrand: brand_id=${brandId}`);
            if (brandId) {
                loadYearsByBrand(brandId);
            }
        });
    }

    if (selectYear) {
        selectYear.addEventListener("change", (e) => {
            const yearId = e.target.value;
            const brandId = selectBrand.value;
            console.log(`📌 Cambio en selectYear: year_id=${yearId}, brand_id=${brandId}`);
            if (yearId && brandId) {
                loadModelsByBrandAndYear(brandId, yearId);
            }
        });
    }

    if (selectModel) {
        selectModel.addEventListener("change", (e) => {
            const modelId = e.target.value;
            const yearId = selectYear.value;
            console.log(`📌 Cambio en selectModel: model_id=${modelId}, year_id=${yearId}`);
            if (modelId && yearId) {
                loadVersions(modelId, yearId);
            }
        });
    }

    imageButtons.forEach((img) => {
        img.addEventListener("click", () => {
            const brandId = img.dataset.brandId;
            console.log(`🖱️ Clic en imagen de marca: brand_id=${brandId}`);
            if (brandId) {
                selectBrand.value = brandId;
                selectBrand.dispatchEvent(new Event("change"));
            }
        });
    });
}, 500);
