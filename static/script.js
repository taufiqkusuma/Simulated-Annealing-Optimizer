document
  .getElementById("saForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const flowMatrix = JSON.parse(document.getElementById("flowMatrix").value);
    const deptSizes = JSON.parse(document.getElementById("deptSizes").value);
    const areaSize = document
      .getElementById("areaSize")
      .value.split(",")
      .map(Number);
    const T_init = parseFloat(document.getElementById("T_init").value);
    const coolingRate = parseFloat(
      document.getElementById("coolingRate").value
    );
    const maxIter = parseInt(document.getElementById("maxIter").value);

    const response = await fetch("/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        flow_matrix: flowMatrix,
        dept_sizes: deptSizes,
        area_size: areaSize,
        T_init,
        cooling_rate: coolingRate,
        max_iter: maxIter,
      }),
    });

    const result = await response.json();
    document.getElementById("result").innerHTML = `
      <h3>Best Layout: ${result.best_layout}</h3>
      <h3>Best Cost: ${result.best_cost}</h3>
  `;
  });
