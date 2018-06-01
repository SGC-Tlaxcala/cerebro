const title = 'Expedientes DPI/USI'

class AvisoExpediente extends React.Component {
  constructor(props) {
    super(props)
    this.expediente = props.expediente
  }

  render() {
    return (
      <div className="alert alert-danger" role="alert">
        Ya existe un expediente con el folio
        <strong>{this.expediente.tipo}_{this.expediente.folio}</strong>
        a nombre de <strong>{this.expediente.nombre}</strong>.
      </div>
    )
  }
}

class Buscador extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      boton: props.boton,
      expediente: {
        tipo: '',
        folio: '',
        nombre: ''
      }
    }
    this.handleInputChange = this.handleInputChange.bind(this)
    this.getInfo = this.getInfo.bind(this)
  }

  handleInputChange = () => {
    this.setState({
      query: this.search.value
    }, () => {
      if (this.state.query && this.state.query.length === 13) {
        this.getInfo()
      }
    })
  }

  getInfo = () => {
    axios.get(`/api/dpi/${this.state.query}/`)
      .then(({data}) => {
        this.setState({
          expediente: data
        })
      })
  }

  renderAviso(){
    if(this.state.expediente.folio.length === 13){
      return (
        <AvisoExpediente expediente={this.state.expediente} />
      )
    } else {
      return (
        <span>&nbsp;</span>
      )
    }
  }

  render() {
    return (
      <div className='buscador'>
        <form>
          <input
            placeholder={'Escribe un folio'}
            maxLength="13"
            ref={input => this.search = input}
            onChange={this.handleInputChange}
          />
          {this.state.query}
        </form>
        <p></p>
        {this.renderAviso()}
      </div>
    )
  }
}

class PageDisplay extends React.Component {
  constructor (props) {
    super()
    this.title = props.title
  }

  render() {
    return(
      <h1 className="display-3">{title}</h1>
    )
  }
}

const App = () => (
  <div id={"app"}>
    <PageDisplay title={title}/>
    <hr/>
    <Buscador boton={'Buscar'} />
  </div>
)

ReactDOM.render(
  <App />,
  document.getElementById('root')
)