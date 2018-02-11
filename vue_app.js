const app = new Vue({
  //Runs on any element with id="app"
  el: '#app',
  data:{
    //All of the information for a risk or multiple risks
    risks: [],
    //The names of all available risks
    risk_list: [],
    //The selected risk to search for when searching for a single risk
    selected: '',
    //The address for the single-risk API without the risk ID
    address: 'https://zzweecos9f.execute-api.us-east-2.amazonaws.com/dev/single-risk?rid='
  },
  methods: {
    //Selects all risks
    all_risks: function(event){
      fetch('https://zzweecos9f.execute-api.us-east-2.amazonaws.com/dev/all-risks')
        .then(response => response.json())
        .then(json => {
          this.risks = json.risks
        })
        //Shows the submit button
        document.getElementById("submit").style.display = "inline";
    },
    //Selects a single risk from the API
    select_risk: function(event){
      for (r in this.risk_list){
        if(this.selected == this.risk_list[r].r_name){
          //Adds the selected risk ID to the end of the API URL
          query_address = this.address + this.risk_list[r].r_id
          fetch(query_address)
            .then(response => response.json())
            .then(json => {
              this.risks = json.risks
            })
        }
      }
      //Shows the submit button
      document.getElementById("submit").style.display = "inline";
    },
    //Hides the submit button
    hide_submit: function(event){
      document.getElementById("submit").style.display = "none";
    }
  },
  //When the app is created, grabs the a list of the available risks
 created(){
    fetch('https://zzweecos9f.execute-api.us-east-2.amazonaws.com/dev/only-risks')
      .then(response => response.json())
      .then(json => {
        this.risk_list = json.risks
      })
      //Hides the submit button
      this.hide_submit()
  }
})
