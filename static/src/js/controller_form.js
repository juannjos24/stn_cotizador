﻿console.log("🟢 Script de cotización cargado correctamente");

setTimeout(() => {
    const imageButtons = document.querySelectorAll("[data-brand-id]");
    const selectBrand = document.querySelector("select[name='brand_id']");
    const selectModel = document.querySelector("select[name='model_id']");
    const selectYear = document.querySelector("select[name='year_id']");
    const selectVersion = document.querySelector("select[name='version_id']");
    const extraFieldsSection = document.querySelector("#extra-fields");    


    const clearAndInit = (select, placeholder) => {
        if (select) {
            select.innerHTML = `<option value="">${placeholder}</option>`;
        }
    };

    const fetchData = async (url, payload) => {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            const json = await response.json();
            if (url === '/api/versions' && json.result?.result) return json.result.result;
            else if (json.result) return Array.isArray(json.result) ? json.result : [];
            return [];
        } catch (error) {
            console.error(`❌ Error en fetch a ${url}:`, error);
            return [];
        }
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
        extraFieldsSection?.classList.add("d-none");
    };

    const loadModelsByBrandAndYear = async (brandId, yearId) => {
        const models = await fetchData('/api/models-by-brand-year', { brand_id: brandId, year_id: yearId });
        clearAndInit(selectModel, "Selecciona un modelo");
        clearAndInit(selectVersion, "Selecciona una versión");
        models.forEach(m => {
            const opt = new Option(m.name, m.id);
            selectModel.appendChild(opt);
        });
        extraFieldsSection?.classList.add("d-none");
    };

    const loadVersions = async (modelId, modelName, yearId) => {
        const versions = await fetchData('/api/versions', {
            model_id: modelId,
            model_name: modelName,
            year_id: yearId
        });
        clearAndInit(selectVersion, "Selecciona una versión");
        if (versions.length > 0) {
            versions.forEach(v => {
                const opt = new Option(v.name, v.id);
                selectVersion.appendChild(opt);
            });
        } else {
            selectVersion.appendChild(new Option("No hay versiones disponibles", ""));
        }
        extraFieldsSection?.classList.add("d-none");
    };

    if (selectBrand) {
        selectBrand.addEventListener("change", (e) => {
            const brandId = e.target.value;
            if (brandId) loadYearsByBrand(brandId);
        });
    }

    if (selectYear) {
        selectYear.addEventListener("change", (e) => {
            const brandId = selectBrand.value;
            const yearId = e.target.value;
            if (brandId && yearId) loadModelsByBrandAndYear(brandId, yearId);
            //console.log();
        });
    }

    if (selectModel) {
        selectModel.addEventListener("change", (e) => {
            const modelId = e.target.value;
            const modelName = e.target.options[e.target.selectedIndex].text;
            const yearId = selectYear.value;
            if (modelId && yearId) loadVersions(modelId, modelName, yearId);
        });
    }

    if (selectVersion) {
        selectVersion.addEventListener("change", () => {
            if (selectVersion.value) {
                extraFieldsSection?.classList.remove("d-none");
            } else {
                extraFieldsSection?.classList.add("d-none");
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

    // 🟩 Selección de tipo de cobertura
    const coverageCards = document.querySelectorAll(".coverage-option");
    const coverageInput = document.querySelector("#type_cobertura");

    coverageCards.forEach(card => {
        card.addEventListener("click", () => {
            coverageCards.forEach(c => c.classList.remove("border-primary", "border-3"));
            card.classList.add("border-primary", "border-3");
            coverageInput.value = card.dataset.value;
        });
    });

    // 🟦 Selección visual de marca con efecto y scroll al formulario
    const brandImages = document.querySelectorAll(".brand-img");

    brandImages.forEach(img => {
        img.addEventListener("click", () => {
            brandImages.forEach(i => {
                i.classList.remove("border-primary", "border-3", "shadow-lg");
            });

            // Estilo al seleccionado
            img.classList.remove("border-dark");
            img.classList.add("border-primary", "border-3", "shadow-lg");


            // Hacer scroll al formulario
            const formulario = document.getElementById("formulario_carros");
            if (formulario) {
                formulario.scrollIntoView({ behavior: "smooth", block: "start" });
            }

            // Opcional: si quieres seleccionar la marca en el select también
            const brandId = img.dataset.brandId;
            const selectBrand = document.querySelector("select[name='brand_id']");
            if (selectBrand && brandId) {
                selectBrand.value = brandId;
                selectBrand.dispatchEvent(new Event("change"));  // si necesitas activar el cambio
            }
        });
    });



}, 500);
