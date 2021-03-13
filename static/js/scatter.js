

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
      bottom: 150,
      right: 50,
      left: 75
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
    var xLabelHeight = svgHeight -100;
    
    
    d3.csv("/static/Top100_zip.csv").then(function(zipdata){
        zipdata.forEach(function(data) {
            data.Median_Income = +data.Median_Income;
            data.Keydemo_per = +data.Keydemo_per * 100;
            data.pop_per_brewery = +data.pop_per_brewery
            data.Starbucks_count = +data.Starbucks_count
            data.Population = +data.Population
            console.log(data.Median_Income)
        });

        
        function getColor(d) {
          return d > 200000 ? '#0000ff' :
                 d > 170000 ? '#1a0fe6' :
                 d > 150000  ? '#331fcc' :
                 d > 140000  ? '#4c2eb2' :
                 d > 130000  ? '#5936a6' :
                 d > 120000  ? '#8c5473' :
                 d > 110000 ? '#995c66' :
                 d > 100000  ? '#b26b4d' :
                 d > 90000  ? '#bf7340' :
                 d > 80000  ? '#d98226' :
                 d > 70000  ? '#f2910d' :
                            '#ff9900';
        }

        var xScale = d3.scaleLinear()
            .domain([0, d3.max(zipdata, d => d.pop_per_brewery)+ 5000])
            .range([0, width]);
        
        var yScale = d3.scaleLinear()
            .domain([0, d3.max(zipdata, d => d.Keydemo_per + .1)])
            .range([height, 0]);

        var xAxis = d3.axisBottom(xScale);
        var yAxis = d3.axisLeft(yScale);

        chartGroup.append("g")
            .attr("transform", `translate(0, ${height})`)
            .call(xAxis);
        
        chartGroup.append("g")
            .call(yAxis)
        
        var circlesGroup = chartGroup.selectAll("circle")
            .data(zipdata)
            .enter()
            .append("circle")
            .attr("cx", d => xScale(d.pop_per_brewery))
            .attr("cy", d => yScale(d.Keydemo_per))
            .attr("r", 15)
            .attr("r", d => d.Population/2500)
            // .style('fill', "green")
            .style('fill', d => getColor(d.Median_Income))
            .style("opacity", 0.9)
            .classed("zipCircle", true);

        var textgroup =chartGroup.selectAll()
            .data(zipdata)
            .enter()
            .append("text")
            .text(d=>d.abbr)
            .attr("x", d => xScale(d.Keydemo_per))
            .attr("y", d=> yScale(d.pop_per_brewery) +4)
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
            .text("Population Per Brewery");
      
      legendColors = ['#0000ff','#1a0fe6', '#331fcc','#4c2eb2','#663d99', '#4c2eb2', '#663d99', '#a66359', '#bf7340', '#d98226', '#f2910d', '#ff9900'];
      legendText = [': >$200,000', ": >$170,000", ": >$150,000", ": >$140,000", ": >$130,000", ": >$120,000", ": >$110,000", ": >$100,000", ": >$90,000", ": >$80,000", ": >$70,000", ": <$70,000"]

      var legend = svg.append("g")
            .attr("transform", `translate(${margin.right}, ${margin.top})`)
            .attr("class", "legend")
            .attr("height", 2000)
            .attr("width", 200)
          
          svg.append('g')
            .attr("transform", `translate(${margin.right}, ${margin.top})`)
            .append("text")
            .attr("x", width- 25)
            .attr("y", 0)
            .attr('text-anchor', 'middle')
            .attr("font-size", "10px")
            .classed("active", true)
            .text("Median Income ($)");
          
          svg.append('g')
            .attr("x", width- 25)
            .attr("y", 0)
            .style("stroke", "lightgreen")
            .style("stroke-width", 10);
          
          legend.selectAll("rect")
            .data(legendColors)
            .enter()
            .append("rect")
            .attr("x", width - 65)
            .attr("y", function(d,i) { return i*20 + 10 })
            .attr("width", 17)
            .attr("height", 17)
            .style("fill", function(d, i) { return legendColors[i]});
          
          legend.selectAll("text")
            .data(legendText)
            .enter()
            .append("text")
            .attr("x", width - 45)
            .attr("y", function(d,i) { return i*20 + 23; })
            .text(function(d, i) { return legendText[i]});

            // Create toolTip
          var toolTip = d3.tip()
            .attr("class", "d3-tip")
            .offset([40,-80])
            .html(function(d) {
              return (`<strong>Zip Code: ${d.PostalCode}<br>Population: ${d.Population}<br>Median Income: $${d.Median_Income}<br>Median Age: ${d.Median_age}<br>Brewery Count: ${d.Brewery_count}<strong>`);
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