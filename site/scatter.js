function makeResponsive() {

    // if the SVG area isn't empty when the browser loads,
    // remove it and replace it with a resized version of the chart
    var svgArea = d3.select("body").select("svg");
  
    // clear svg is not empty
    if (!svgArea.empty()) {
      svgArea.remove();
    }
  
    var svgWidth = window.innerWidth;
    var svgHeight = window.innerHeight;
  
    var margin = {
      top: 50,
      bottom: 50,
      right: 50,
      left: 60
    };
  
    var height = svgHeight - margin.top - margin.bottom;
    var width = svgWidth - margin.left - margin.right;

    var svg = d3
        .select("#scatter")
        .append("svg")
        .attr("viewBox", `0 0 ${svgWidth} ${svgHeight}`)
        // .attr("height", svgHeight)
        // .attr("width", svgWidth);

    var chartGroup = svg.append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);

    
    var yLabelWidth = 15;
    var yLabelHeight = svgHeight / 2;

    var xLabelWidth = svgWidth / 2;
    var xLabelHeight = svgHeight -10;
    
    d3.csv('/brewBuds_project2/income_data/Top100_zip.csv').then(function(zipdata){
        zipdata.forEach(function(data) {
            data.Median_Income = +data.Median_Income;
            data.Keydemo_per = +data.Keydemo_per * 100;
            console.log(data.Median_Income)
        });
        
        var xScale = d3.scaleLinear()
            .domain([0, d3.max(zipdata, d => d.Median_Income) + 1000])
            .range([0, width]);
        
        var yScale = d3.scaleLinear()
            .domain([0, d3.max(zipdata, d => d.Keydemo_per)])
            .range([height, 0]);

        var xAxis = d3.axisBottom(xScale);
        var yAxis = d3.axisLeft(yScale)

        chartGroup.append("g")
            .attr("transform", `translate(0, ${height})`)
            .call(xAxis);
        
        chartGroup.append("g")
            .call(yAxis)
        
        var circlesGroup = chartGroup.selectAll("circle")
            .data(zipdata)
            .enter()
            .append("circle")
            .attr("cx", d => xScale(d.Median_Income))
            .attr("cy", d => yScale(d.Keydemo_per))
            .attr("r", "15")
            .classed("zipCircle", true);
            
        var textgroup =chartGroup.selectAll()
            .data(zipdata)
            .enter()
            .append("text")
            .text(d=>d.abbr)
            .attr("x", d => xScale(d.Median_Income))
            .attr("y", d=> yScale(d.Keydemo_per) +4)
            .attr("font-size", "10px")
            .classed("stateText", true);
  
        svg.append('g')
            .attr("transform", `translate(${yLabelWidth}, ${yLabelHeight} )`)
            .append("text")
            .attr('text-anchor', 'middle')
            .attr("transform", 'rotate(-90)')
            .attr("font-size", "20px")
            .classed("active", true)
            .text("Key Demo (%)");
        
            svg.append('g')
            .attr("transform", `translate(${xLabelWidth}, ${xLabelHeight} )`)
            .append("text")
            .attr('text-anchor', 'middle')
            .attr("font-size", "20px")
            .classed("active", true)
            .text("Median Income ($)");
    
          // Create toolTip
          var toolTip = d3.tip()
            .attr("class", "d3-tip")
            .offset([40,-80])
            .html(function(d) {
              return (`<strong>Zip Code: ${d.PostalCode}<br>Median Income: $${d.Median_Income}<br>Key Demo: ${d.Keydemo_per}%<strong>`);
            });
           
          chartGroup.call(toolTip);
    
          
          circlesGroup.on("mouseover", function(d) {
            toolTip.show(d, this);
            d3.select(this).style("stroke", "black");
           
          })
            .on("mouseout", function(d) {
              toolTip.hide(d);
              d3.select(this).style("stroke", "white");
            });
  
          textgroup.on("mouseover", function(d) {
            tooltip.show(d, this);
            d3.select(this).style("stroke", "black");
          })
            .on("mouseout", function(d) {
              tooltip.hide(d);
              d3.select(this).style("stroke", "white");
        });
    });
    
};

makeResponsive();
d3.select(window).on("resize", makeResponsive);