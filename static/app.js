
var game = new Chess()
var $status = $('#status')
var $fen = $('#fen')
var whiteSquareGrey = '#a9a9a9'
var blackSquareGrey = '#696969'
var squareClass = 'square-55d63'
var squareToHighlight = null
var colorToHighlight = null
var $board = $('#myBoard')



function removeGreySquares () {
  $('#myBoard .square-55d63').css('background', '')
}

function greySquare (square) {
  var $square = $('#myBoard .square-' + square)

  var background = whiteSquareGrey
  if ($square.hasClass('black-3c85d')) {
    background = blackSquareGrey
  }

  $square.css('background', background)
}



function onDragStart (source, piece, position, orientation) {
  // do not pick up pieces if the game is over
  if (game.game_over()) return false

  // only pick up pieces for the side to move
  if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
      (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
    return false
  }
}
function reset_show_move() {

	    $board.find('.' + squareClass).removeClass('highlight-white')
	    $board.find('.' + squareClass).removeClass('highlight-black')
	    $board.find('.square-' + squareToHighlight).removeClass('highlight-' + colorToHighlight)
}
function show_move (move) {

  if (move.color === 'w') {
	    $board.find('.' + squareClass).removeClass('highlight-white')
	    $board.find('.square-' + move.from).addClass('highlight-white')

	    $board.find('.square-' + move.to).addClass('highlight-white')
  } else {
	    $board.find('.' + squareClass).removeClass('highlight-black')
	    $board.find('.square-' + move.from).addClass('highlight-black')
	    $board.find('.square-' + move.to).addClass('highlight-black')
  }
}
function onDrop (source, target) {
  // see if the move is legal
  var move = game.move({
    from: source,
    to: target,
    promotion: 'q' // NOTE: always promote to a queen for example simplicity
  })

  // illegal move
  if (move === null) return 'snapback'
  show_move(move) 
	
  $.post("/human_play",{"fen":game.fen()},function(data){var move = game.move(data);board.position(game.fen().split(' ')[0]);show_move(move),updateStatus()})
	
	
}
function onMouseoverSquare (square, piece) {
  // get list of possible moves for this square
  var moves = game.moves({
    square: square,
    verbose: true
  })

  // exit if there are no moves available for this square
  if (moves.length === 0) return

  // highlight the square they moused over
  greySquare(square)

  // highlight the possible squares for this piece
  for (var i = 0; i < moves.length; i++) {
    greySquare(moves[i].to)
  }
}

function onMouseoutSquare (square, piece) {
  removeGreySquares()
}

// update the board position after the piece snap
// for castling, en passant, pawn promotion
function onSnapEnd () {
  board.position(game.fen().split(' ')[0])

}

function updateStatus () {
  var status = ''
  var moveColor = 'White'
  if (game.turn() === 'b') {
    moveColor = 'Black'
  }

  // checkmate?
  if (game.in_checkmate()) {
    status = 'Game over, ' + moveColor + ' is in checkmate.'
  }

  // draw?
  else if (game.in_draw()) {
    status = 'Game over, drawn position'
  }

  // game still on
  else {
    status = moveColor + ' to move'

    // check?
    if (game.in_check()) {
      status += ', ' + moveColor + ' is in check'
    }
  }

  $status.html(status)
  $fen.html(game.fen())
}


var config = {
  draggable: true,
  position: 'start',
  onDragStart: onDragStart,
  onDrop: onDrop,
  onSnapEnd: onSnapEnd,
  onMouseoutSquare: onMouseoutSquare,
  onMouseoverSquare: onMouseoverSquare,
  pieceTheme: 'static/img/chesspieces/wikipedia/{piece}.png'
}





var board = Chessboard('myBoard', config)
updateStatus()
$('#selfplay').click(function(){
	$.get('/selfplay',function(data){
		var jo = $.parseJSON(data)
		$('#selfplay').data('playlist',jo)
		$('#pre').data('index',-1).show()
		$('#next').data('len',jo.length-1).show()
		game.reset()
		config.draggable = false
	        delete config.onMouseoutSquare
	  	delete config.onMouseoverSquare
		board = Chessboard('myBoard',config)
		reset_show_move()
	})
})
$('#pre').click(function(){
	var index = $(this).data('index')
	var nx = index -1
	if (nx<-1) return
	var move = game.undo()
	show_move(move)
	board.position(game.fen().split(' ')[0])
	$('#pre').data('index',nx)
	updateStatus()
	$('#run_number').html(nx)
})
$('#next').click(function(){
	var index = $('#pre').data('index')
	var len  = $('#next').data('len')
	index = ((index+1)>len?len:(index+1)) 
	san = $('#selfplay').data('playlist')[index]
	console.log(san)
	var move = game.move(san)
	show_move(move)
	board.position(game.fen().split(' ')[0])
	$('#pre').data('index',index)
	updateStatus()
	$('#run_number').html(index)
})
$('#manul').click(function(){
	config.draggable = true
	config.onMouseoutSquare= onMouseoutSquare
	config.onMouseoverSquare= onMouseoverSquare
	board = Chessboard('myBoard',config)
	$('#pre').hide()
	$('#next').hide()
	$('#run_number').html('')
	game.reset()
})
