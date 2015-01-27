# booklet -p 0-99 -s 5
# -p	Pages (default all)
# -s	Sheets per "page group" (find correct term) (default auto = as many as is required to fit all pages)

def test_pagegroups():
	assert pagegroups( 1 ) == 1
	assert pagegroups( 2 ) == 1
	assert pagegroups( 3 ) == 1
	assert pagegroups( 4 ) == 1

	assert pagegroups( 5 ) == 2
	assert pagegroups( 6 ) == 2
	assert pagegroups( 7 ) == 2
	assert pagegroups( 8 ) == 2
	
	assert pagegroups( 16 ) == 4


def test_pagesequence():
	pagesequence = iter_pages( 4 )
	assert pagesequence.next() == 1
	assert pagesequence.next() == 2
	assert pagesequence.next() == 3
	assert pagesequence.next() == 4

	pagesequence = iter_pages( 8 )
	assert pagesequence.next() == 1
	assert pagesequence.next() == 2
	assert pagesequence.next() == 7
	assert pagesequence.next() == 8
	assert pagesequence.next() == 3
	assert pagesequence.next() == 4
	assert pagesequence.next() == 5
	assert pagesequence.next() == 6

	pagesequence = iter_pages( 16 )
	assert pagesequence.next() == 1
	assert pagesequence.next() == 2
	assert pagesequence.next() == 15
	assert pagesequence.next() == 16
	assert pagesequence.next() == 3
	assert pagesequence.next() == 4
	assert pagesequence.next() == 13
	assert pagesequence.next() == 14
	assert pagesequence.next() == 5
	assert pagesequence.next() == 6
	assert pagesequence.next() == 11
	assert pagesequence.next() == 12
	assert pagesequence.next() == 7
	assert pagesequence.next() == 8
	assert pagesequence.next() == 9
	assert pagesequence.next() == 10

if __name__ == '__main__':
	test_pagesequence()