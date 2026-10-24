import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import BookForm from './BookForm.jsx'

afterEach(cleanup)

describe('BookForm', () => {
  it('menampilkan pesan jika judul dan penulis kosong', () => {
    render(<BookForm book={null} onSave={vi.fn()} onCancel={vi.fn()} />)

    fireEvent.click(screen.getByRole('button', { name: 'Tambah buku' }))

    expect(screen.getByText('Judul buku wajib diisi.')).toBeInTheDocument()
    expect(screen.getByText('Nama penulis wajib diisi.')).toBeInTheDocument()
  })

  it('mengirim data buku yang sudah diisi', () => {
    const onSave = vi.fn()
    render(<BookForm book={null} onSave={onSave} onCancel={vi.fn()} />)

    fireEvent.change(screen.getByLabelText('Judul buku'), { target: { value: 'Bumi Manusia' } })
    fireEvent.change(screen.getByLabelText('Penulis'), { target: { value: 'Pramoedya Ananta Toer' } })
    fireEvent.change(screen.getByLabelText('Status buku'), { target: { value: 'reading' } })
    fireEvent.click(screen.getByRole('button', { name: 'Tambah buku' }))

    expect(onSave).toHaveBeenCalledWith({
      title: 'Bumi Manusia',
      author: 'Pramoedya Ananta Toer',
      status: 'reading',
    })
  })
})
