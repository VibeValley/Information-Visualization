function combineEpisodes() {
    let allData = [];
  //C:\Users\xgujo\GitHubRepos\my-netflix\Information-Visualization\assignment4\starwars-intercation\starwars-episode-1-interactions-allCharacters.json
    for (let i = 1; i < 8; i++) {
      d3.json(`./starwars-interaction/starwars-episode-${i}-interactions-allCharacters.json`,
        (data) => {
          // Update source and target id to name
          data.links.map((link) => {
            link.source = data.nodes[link.source].name;
            link.target = data.nodes[link.target].name;
          });
  
          allData.push(data);
        }
      );
    }
  
    // let combinedData = { nodes, links };
  
    return allData;
  }
  
  let allData = combineEpisodes();

  console.log(allData);